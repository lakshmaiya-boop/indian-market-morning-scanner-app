from __future__ import annotations

from datetime import datetime
from typing import Any

from app.services.mock_adapter import MockMarketDataAdapter


class StockScanner:
    def __init__(self, adapter: MockMarketDataAdapter | None = None) -> None:
        self.adapter = adapter or MockMarketDataAdapter()

    def scan_stocks(self, symbols: list[str]) -> list[dict[str, Any]]:
        reports: list[dict[str, Any]] = []
        for symbol in symbols:
            snapshot = self.adapter.get_price_snapshot(symbol)
            score = self._score_from_snapshot(snapshot)
            verdict = self._verdict_from_score(score)
            reasons = [
                "Trend remains constructive with support holding above key moving averages.",
                "Volume remains above the 20-day average with improving participation.",
                "News sentiment is positive and the price structure remains above breakout support.",
            ]
            trade_plan = {
                "strategy": "EMA pullback",
                "entry": round(snapshot["close"] * 0.995, 2),
                "target_1": round(snapshot["resistance"], 2),
                "target_2": round(snapshot["resistance"] * 1.04, 2),
                "stop_loss": round(snapshot["support"], 2),
                "rr_ratio": 2.3,
            }
            reports.append(
                {
                    "symbol": symbol,
                    "score": score,
                    "verdict": verdict,
                    "reasons": reasons,
                    "support": snapshot["support"],
                    "resistance": snapshot["resistance"],
                    "news_sentiment": snapshot["sentiment"],
                    "impact": "moderate",
                    "trade_plan": trade_plan,
                    "disclaimer": "For educational and informational purposes only, not investment advice. Trading in stocks, F&O and commodities carries high risk. Consult a SEBI-registered advisor.",
                }
            )
        return reports

    def _score_from_snapshot(self, snapshot: dict[str, Any]) -> int:
        base = int(snapshot["score"])
        if snapshot["sentiment"] == "bullish":
            base += 10
        return max(0, min(100, base))

    def _verdict_from_score(self, score: int) -> str:
        if score >= 85:
            return "Strong Bull"
        if score >= 70:
            return "Bull"
        if score >= 55:
            return "Neutral"
        if score >= 35:
            return "Bear"
        return "Strong Bear"

    def get_report_for_symbol(self, symbol: str) -> dict[str, Any]:
        snapshot = self.adapter.get_price_snapshot(symbol)
        score = self._score_from_snapshot(snapshot)
        verdict = self._verdict_from_score(score)
        news = self.adapter.get_news(symbol)
        return {
            "symbol": symbol,
            "name": symbol,
            "score": score,
            "verdict": verdict,
            "reasons": [
                "Trend remains firm on the daily timeframe.",
                "Price is holding above support area.",
                "Volume is supportive and the headline outlook is constructive.",
            ],
            "support": snapshot["support"],
            "resistance": snapshot["resistance"],
            "news_sentiment": news["sentiment"],
            "impact": news["impact"],
            "trade_plan": {
                "strategy": "EMA pullback",
                "entry": round(snapshot["close"] * 0.996, 2),
                "target_1": round(snapshot["resistance"], 2),
                "target_2": round(snapshot["resistance"] * 1.05, 2),
                "stop_loss": round(snapshot["support"], 2),
                "rr_ratio": 2.4,
            },
            "disclaimer": "For educational and informational purposes only, not investment advice. Trading in stocks, F&O and commodities carries high risk. Consult a SEBI-registered advisor.",
        }
