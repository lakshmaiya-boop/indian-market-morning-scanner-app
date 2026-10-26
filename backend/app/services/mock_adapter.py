from __future__ import annotations

from datetime import datetime
from typing import Any, Literal


class MockMarketDataAdapter:
    """Pluggable market-data adapter with a mock implementation for local development."""

    def __init__(self) -> None:
        self.nifty50 = [
            "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "ITC", "SBIN", "LTIM", "HINDUNILVR",
            "BAJFINANCE", "AXISBANK", "KOTAKBANK", "SUNPHARMA", "TITAN", "BHARTIARTL", "NTPC", "WIPRO",
            "ASIANPAINT", "POWERGRID", "HCLTECH", "ULTRACEMCO", "SBILIFE", "M&M", "INDUSINDBK",
            "TECHM", "TATAMOTORS", "ONGC", "MARUTI", "CIPLA", "NESTLEIND", "GRASIM", "JSWSTEEL",
            "HINDALCO", "APOLLOHOSP", "DRREDDY", "TATASTEEL", "COALINDIA", "EICHERMOT", "ADANIPORTS",
            "BPCL", "SHRIRAMFIN", "HEROMOTOCO", "LT", "BAJAJ-AUTO", "BRITANNIA", "IOC", "DMART",
        ]
        self.nifty500 = [
            "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "ITC", "SBIN", "LTIM", "HINDUNILVR",
            "BAJFINANCE", "AXISBANK", "KOTAKBANK", "SUNPHARMA", "TITAN", "BHARTIARTL", "NTPC", "WIPRO",
            "ASIANPAINT", "POWERGRID", "HCLTECH", "ULTRACEMCO", "SBILIFE", "M&M", "INDUSINDBK",
            "TECHM", "TATAMOTORS", "ONGC", "MARUTI", "CIPLA", "NESTLEIND", "JSWSTEEL", "HINDALCO",
            "TATASTEEL", "ADANIPORTS", "SHRIRAMFIN", "LT", "BAJAJ-AUTO", "BRITANNIA", "DMART",
            "GAIL", "AARTIIND", "GODREJPROP", "DABUR", "PIDILITIND", "NMDC", "TRENT", "METROPOLIS",
            "JUBLFOOD", "IRCTC", "PAGEIND", "SYNGENE", "BANDHANBNK", "ZYDUSLIFE", "GODREJCP",
        ]
        self.watchlist = ["RELIANCE", "TCS", "HDFCBANK", "INFY", "BAJFINANCE"]
        self.base_prices = {
            "RELIANCE": 2950.0,
            "TCS": 3940.0,
            "INFY": 1490.0,
            "HDFCBANK": 1715.0,
            "ICICIBANK": 1238.0,
            "ITC": 454.0,
            "SBIN": 864.0,
            "LTIM": 6058.0,
            "HINDUNILVR": 2625.0,
            "BAJFINANCE": 6760.0,
            "AXISBANK": 1140.0,
            "KOTAKBANK": 1848.0,
            "SUNPHARMA": 1415.0,
            "TITAN": 3417.0,
            "BHARTIARTL": 1458.0,
            "NTPC": 382.0,
            "WIPRO": 540.0,
            "ASIANPAINT": 3180.0,
            "POWERGRID": 288.0,
            "HCLTECH": 1685.0,
            "ULTRACEMCO": 11180.0,
            "SBILIFE": 1645.0,
            "M&M": 2878.0,
            "INDUSINDBK": 1550.0,
            "TECHM": 1510.0,
            "TATAMOTORS": 912.0,
            "ONGC": 282.0,
            "MARUTI": 11238.0,
            "CIPLA": 1530.0,
            "NESTLEIND": 2614.0,
            "GRASIM": 2528.0,
            "JSWSTEEL": 960.0,
            "HINDALCO": 662.0,
            "APOLLOHOSP": 6564.0,
            "DRREDDY": 6290.0,
            "TATASTEEL": 152.0,
            "COALINDIA": 470.0,
            "EICHERMOT": 4844.0,
            "ADANIPORTS": 1320.0,
            "BPCL": 333.0,
            "SHRIRAMFIN": 2320.0,
            "HEROMOTOCO": 5730.0,
            "LT": 3635.0,
            "BAJAJ-AUTO": 8378.0,
            "BRITANNIA": 5200.0,
            "IOC": 148.0,
            "DMART": 4140.0,
        }
        self.meta = {
            "NIFTY_50": {"index": 24500.0, "change_pct": 0.65},
            "NIFTY_500": {"index": 22780.0, "change_pct": 0.40},
        }

    def get_instruments(self, section: str | None = None) -> list[str]:
        symbols = list(self.nifty50)
        if section == "stocks":
            return symbols + self.watchlist
        return symbols

    def get_price_snapshot(self, symbol: str) -> dict[str, Any]:
        price = self.base_prices.get(symbol, 100.0)
        drift = 0.03 if symbol in {"RELIANCE", "INFY", "TCS"} else 0.015
        close = price * (1 + drift)
        support = close * 0.97
        resistance = close * 1.03
        return {
            "symbol": symbol,
            "close": round(close, 2),
            "support": round(support, 2),
            "resistance": round(resistance, 2),
            "volume": 1500000,
            "avg_volume": 1000000,
            "score": 68,
            "sentiment": "bullish",
            "verdict": "Bull",
            "news_summary": "Positive earnings and improving sector breadth support this setup.",
        }

    def get_global_snapshot(self) -> dict[str, Any]:
        return {
            "global": {
                "dxy": 103.9,
                "us_10y_yield": 4.18,
                "us_2y_yield": 4.02,
                "gift_nifty": 24480.0,
                "crude": 78.4,
                "gold": 2448.0,
            },
            "events": [
                {"event_name": "US CPI", "time_ist": "08:30 IST", "impact": "High", "summary": "Inflation prints may influence risk sentiment and DXY.", "affected_symbols": ["RELIANCE", "TCS", "GOLD", "CRUDE"]},
                {"event_name": "Fed Decision", "time_ist": "18:00 IST", "impact": "High", "summary": "Policy guidance could affect financials and commodity sentiment.", "affected_symbols": ["HDFCBANK", "ICICIBANK", "GOLD", "COPPER"]},
                {"event_name": "RBI Policy", "time_ist": "10:00 IST", "impact": "Medium", "summary": "Liquidity and rates remain watchpoints for banking and rates-sensitive sectors.", "affected_symbols": ["SBIN", "HDFCBANK", "LTIM"]},
            ],
        }

    def strategy_scorecard(self) -> list[dict[str, Any]]:
        return [
            {"strategy": "EMA pullback", "trades": 52, "win_rate": 0.54, "avg_rr": 1.6, "max_drawdown": 12.0, "expectancy": 0.7, "enabled": True},
            {"strategy": "Opening range breakout", "trades": 34, "win_rate": 0.49, "avg_rr": 1.4, "max_drawdown": 15.5, "expectancy": 0.4, "enabled": True},
            {"strategy": "S/R bounce + OI", "trades": 28, "win_rate": 0.52, "avg_rr": 1.7, "max_drawdown": 11.2, "expectancy": 0.9, "enabled": True},
        ]

    def get_news(self, symbol: str) -> dict[str, Any]:
        return {
            "headline": f"{symbol} sees stable sector sentiment as key support broadens.",
            "sentiment": "positive",
            "impact": "moderate",
            "reasoning": "Positive earnings tone, improving market breadth, and stable macro cues support a constructive setup.",
        }

    def get_watchlist(self) -> list[str]:
        return self.watchlist

    def add_watchlist(self, symbol: str) -> list[str]:
        if symbol not in self.watchlist:
            self.watchlist.append(symbol)
        return self.watchlist
