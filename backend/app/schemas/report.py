from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any


class TradePlanSchema(BaseModel):
    strategy: str
    entry: float
    target_1: float
    target_2: float
    stop_loss: float
    rr_ratio: float


class ReportCard(BaseModel):
    symbol: str
    score: int = Field(ge=0, le=100)
    verdict: str
    reasons: list[str]
    support: float | None = None
    resistance: float | None = None
    news_sentiment: str
    impact: str
    trade_plan: TradePlanSchema
    disclaimer: str


class InstrumentAnalysis(BaseModel):
    symbol: str
    name: str
    score: int
    verdict: str
    reasons: list[str]
    support: float
    resistance: float
    news_sentiment: str
    impact: str
    trade_plan: TradePlanSchema
    disclaimer: str


class StrategyScorecard(BaseModel):
    strategy: str
    trades: int
    win_rate: float
    avg_rr: float
    max_drawdown: float
    expectancy: float
    enabled: bool


class WatchlistItem(BaseModel):
    symbol: str


class DeviceRegistration(BaseModel):
    token: str
    platform: str = "android"
    user_id: int = 1


class GlobalEvent(BaseModel):
    event_name: str
    time_ist: str
    impact: str
    summary: str
    affected_symbols: list[str]
