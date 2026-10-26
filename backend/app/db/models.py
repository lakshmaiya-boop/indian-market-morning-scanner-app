from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Instrument(Base):
    __tablename__ = "instruments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    exchange: Mapped[str] = mapped_column(String(50), default="NSE")
    segment: Mapped[str] = mapped_column(String(50), default="stocks")
    sector: Mapped[str] = mapped_column(String(100), nullable=True)
    industry: Mapped[str] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    price_data: Mapped[list["PriceData"]] = relationship(back_populates="instrument")
    news: Mapped[list["NewsItem"]] = relationship(back_populates="instrument")
    watchlist_entries: Mapped[list["Watchlist"]] = relationship(back_populates="instrument")


class PriceData(Base):
    __tablename__ = "price_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    instrument_id: Mapped[int] = mapped_column(ForeignKey("instruments.id"), nullable=False)
    symbol: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    ts: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)
    open: Mapped[float] = mapped_column(Float, nullable=False)
    high: Mapped[float] = mapped_column(Float, nullable=False)
    low: Mapped[float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[int] = mapped_column(Integer, default=0)
    avg_volume: Mapped[int] = mapped_column(Integer, default=0)
    instrument: Mapped[Instrument] = relationship(back_populates="price_data")


class OptionChain(Base):
    __tablename__ = "option_chain"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    expiry: Mapped[str] = mapped_column(String(30), nullable=False)
    strike: Mapped[float] = mapped_column(Float, nullable=False)
    option_type: Mapped[str] = mapped_column(String(10), nullable=False)
    oi: Mapped[int] = mapped_column(Integer, default=0)
    volume: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class NewsItem(Base):
    __tablename__ = "news_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    instrument_id: Mapped[int | None] = mapped_column(ForeignKey("instruments.id"), nullable=True)
    symbol: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    headline: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(100), default="unknown")
    published_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    sentiment: Mapped[str] = mapped_column(String(50), default="neutral")
    instrument: Mapped[Instrument | None] = relationship(back_populates="news")


class NewsAnalysis(Base):
    __tablename__ = "news_analysis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    sentiment: Mapped[str] = mapped_column(String(50), default="neutral")
    impact: Mapped[str] = mapped_column(String(50), default="moderate")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    reasoning: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class DailyReport(Base):
    __tablename__ = "daily_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    section: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    symbol: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    report_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    score: Mapped[int] = mapped_column(Integer, default=50)
    verdict: Mapped[str] = mapped_column(String(50), default="Neutral")
    reasons: Mapped[str] = mapped_column(Text, default="")
    support: Mapped[float | None] = mapped_column(Float, nullable=True)
    resistance: Mapped[float | None] = mapped_column(Float, nullable=True)
    trade_plan_json: Mapped[str] = mapped_column(Text, default="{}")
    disclaimer: Mapped[str] = mapped_column(Text, default="For educational and informational purposes only, not investment advice. Trading in stocks, F&O and commodities carries high risk. Consult a SEBI-registered advisor.")


class TradePlan(Base):
    __tablename__ = "trade_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    section: Mapped[str] = mapped_column(String(20), nullable=False)
    symbol: Mapped[str] = mapped_column(String(50), nullable=False)
    strategy: Mapped[str] = mapped_column(String(80), default="ema_pullback")
    entry: Mapped[float] = mapped_column(Float, nullable=False)
    target_1: Mapped[float] = mapped_column(Float, nullable=False)
    target_2: Mapped[float] = mapped_column(Float, nullable=False)
    stop_loss: Mapped[float] = mapped_column(Float, nullable=False)
    rr_ratio: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Strategy(Base):
    __tablename__ = "strategies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    section: Mapped[str] = mapped_column(String(20), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    description: Mapped[str] = mapped_column(Text, default="")
    config_json: Mapped[str] = mapped_column(Text, default="{}")
    backtest_summary_json: Mapped[str] = mapped_column(Text, default="{}")
    live_scorecard_json: Mapped[str] = mapped_column(Text, default="{}")


class StrategyTrade(Base):
    __tablename__ = "strategy_trades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    strategy_id: Mapped[int] = mapped_column(ForeignKey("strategies.id"), nullable=False)
    symbol: Mapped[str] = mapped_column(String(50), nullable=False)
    trade_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    outcome: Mapped[str] = mapped_column(String(30), default="open")
    pnl: Mapped[float] = mapped_column(Float, default=0.0)
    rr_ratio: Mapped[float] = mapped_column(Float, default=0.0)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Watchlist(Base):
    __tablename__ = "watchlists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, default=1)
    instrument_id: Mapped[int | None] = mapped_column(ForeignKey("instruments.id"), nullable=True)
    symbol: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    instrument: Mapped[Instrument | None] = relationship(back_populates="watchlist_entries")


class DeviceToken(Base):
    __tablename__ = "device_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, default=1)
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    platform: Mapped[str] = mapped_column(String(30), default="android")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
