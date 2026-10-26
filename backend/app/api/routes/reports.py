from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import DailyReport, Instrument, Watchlist
from app.services.mock_adapter import MockMarketDataAdapter
from app.services.scanner import StockScanner

router = APIRouter(prefix="", tags=["market"])
adapter = MockMarketDataAdapter()
scanner = StockScanner(adapter)


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "indian-market-morning-scanner"}


@router.get("/reports/today")
def get_today_reports(section: str = Query(default="stocks"), db: Session = Depends(get_db)) -> dict[str, object]:
    if section not in {"stocks", "fno", "mcx"}:
        raise HTTPException(status_code=400, detail="section must be one of: stocks, fno, mcx")

    if section == "stocks":
        symbols = adapter.get_instruments(section)
        findings = scanner.scan_stocks(symbols)
    else:
        findings = [
            {
                "symbol": "NIFTY" if section == "fno" else "GOLD",
                "score": 66,
                "verdict": "Bull",
                "reasons": ["Macro backdrop remains constructive for the chosen segment.", "Key levels are holding with moderate momentum."],
                "support": 24350.0 if section == "fno" else 2440.0,
                "resistance": 24700.0 if section == "fno" else 2475.0,
                "news_sentiment": "positive",
                "impact": "moderate",
                "trade_plan": {
                    "strategy": "range breakout" if section == "fno" else "supertrend+rsi",
                    "entry": 24460.0 if section == "fno" else 2455.0,
                    "target_1": 24780.0 if section == "fno" else 2488.0,
                    "target_2": 24900.0 if section == "fno" else 2515.0,
                    "stop_loss": 24310.0 if section == "fno" else 2438.0,
                    "rr_ratio": 2.2,
                },
                "disclaimer": "For educational and informational purposes only, not investment advice. Trading in stocks, F&O and commodities carries high risk. Consult a SEBI-registered advisor.",
            }
        ]

    return {"section": section, "reports": findings, "generated_at": __import__("datetime").datetime.utcnow().isoformat()}


@router.get("/instruments/{symbol}/analysis")
def get_instrument_analysis(symbol: str, db: Session = Depends(get_db)) -> dict[str, object]:
    normalized = symbol.upper()
    if normalized not in adapter.base_prices and normalized not in adapter.nifty50 and normalized not in adapter.watchlist:
        raise HTTPException(status_code=404, detail=f"Instrument {symbol} not found in mock dataset")
    report = scanner.get_report_for_symbol(normalized)
    return report


@router.get("/global-events")
def get_global_events() -> dict[str, object]:
    return adapter.get_global_snapshot()


@router.get("/strategies/scorecard")
def get_scorecard() -> dict[str, object]:
    return {"strategies": adapter.strategy_scorecard(), "generated_at": __import__("datetime").datetime.utcnow().isoformat()}


@router.get("/watchlist")
def get_watchlist() -> dict[str, object]:
    return {"symbols": adapter.get_watchlist()}


@router.post("/watchlist")
def add_watchlist(symbol: str, db: Session = Depends(get_db)) -> dict[str, object]:
    if not symbol:
        raise HTTPException(status_code=400, detail="symbol is required")
    watchlist = adapter.add_watchlist(symbol.upper())
    return {"symbols": watchlist}


@router.post("/devices/register")
def register_device(token: str, platform: str = "android", user_id: int = 1, db: Session = Depends(get_db)) -> dict[str, object]:
    if not token:
        raise HTTPException(status_code=400, detail="token is required")
    return {"status": "registered", "token": token, "platform": platform, "user_id": user_id}
