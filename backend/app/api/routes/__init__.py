from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.mock_adapter import MockMarketDataAdapter
from app.services.scanner import StockScanner

router = APIRouter(tags=["reports"])
adapter = MockMarketDataAdapter()
scanner = StockScanner(adapter)


@router.get("/reports/today")
def get_reports_today(section: str = Query(default="stocks"), db: Session = Depends(get_db)) -> dict[str, object]:
    if section not in {"stocks", "fno", "mcx"}:
        raise HTTPException(status_code=400, detail="section must be stocks, fno or mcx")

    if section == "stocks":
        symbols = adapter.get_instruments(section)
        reports = scanner.scan_stocks(symbols)
    else:
        reports = [{
            "symbol": "NIFTY" if section == "fno" else "GOLD",
            "score": 66,
            "verdict": "Bull",
            "reasons": ["The trend is constructive and the segment is holding above support.", "Options flow and macro backdrop remain supportive."],
            "support": 24450.0 if section == "fno" else 2445.0,
            "resistance": 24780.0 if section == "fno" else 2482.0,
            "news_sentiment": "positive",
            "impact": "moderate",
            "trade_plan": {
                "strategy": "range breakout" if section == "fno" else "supertrend+rsi",
                "entry": 24580.0 if section == "fno" else 2460.0,
                "target_1": 24850.0 if section == "fno" else 2490.0,
                "target_2": 25080.0 if section == "fno" else 2518.0,
                "stop_loss": 24370.0 if section == "fno" else 2430.0,
                "rr_ratio": 2.2,
            },
            "disclaimer": "For educational and informational purposes only, not investment advice. Trading in stocks, F&O and commodities carries high risk. Consult a SEBI-registered advisor.",
        }]

    return {"section": section, "reports": reports}


@router.get("/instruments/{symbol}/analysis")
def get_instrument_analysis(symbol: str) -> dict[str, object]:
    normalized = symbol.upper()
    report = scanner.get_report_for_symbol(normalized)
    return report


@router.get("/global-events")
def get_global_events() -> dict[str, object]:
    return adapter.get_global_snapshot()


@router.get("/strategies/scorecard")
def get_strategy_scorecard() -> dict[str, object]:
    return {"strategies": adapter.strategy_scorecard()}


@router.get("/watchlist")
def get_watchlist() -> dict[str, list[str]]:
    return {"symbols": adapter.get_watchlist()}


@router.post("/watchlist")
def add_watchlist(symbol: str) -> dict[str, list[str]]:
    return {"symbols": adapter.add_watchlist(symbol.upper())}


@router.post("/devices/register")
def register_device(token: str, platform: str = "android", user_id: int = 1) -> dict[str, object]:
    return {"status": "registered", "token": token, "platform": platform, "user_id": user_id}
