# Indian Market Morning Scanner

## Phase 1 status

This repository contains the Phase 1 backend skeleton for the Indian Market Morning Scanner project. It includes:

- FastAPI service skeleton
- PostgreSQL/Redis/Celery-ready configuration
- SQLAlchemy database models for all required tables
- mock market data adapter with sample Indian equities and macro data
- STOCKS scanner and API endpoints
- tests for the scanner and report generation
- Docker Compose and environment setup for local development

## Architecture overview

- Backend: FastAPI + SQLAlchemy + Pydantic
- Runtime: PostgreSQL + Redis + Celery
- Market data layer: pluggable adapter interface with mock adapter that works without API keys
- Analysis layer: scanner computes stock-level verdicts, support/resistance, and trade plans

## Quick start

1. Copy `.env.example` to `.env`.
2. Start dependencies:

```bash
docker compose up -d postgres redis
```

3. Install Python dependencies:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. Start the application:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. Open the API docs:

- http://localhost:8000/docs
- http://localhost:8000/redoc

## API examples

```bash
curl "http://localhost:8000/reports/today?section=stocks"
curl "http://localhost:8000/instruments/RELIANCE/analysis"
curl "http://localhost:8000/strategies/scorecard"
```

## Disclaimer

For educational and informational purposes only, not investment advice. Trading in stocks, F&O and commodities carries high risk. Consult a SEBI-registered advisor.

## Notes

- Phase 2 will add the Next.js dashboard UI.
- Phase 3 adds F&O and MCX engines.
- Phase 4 adds Claude-powered news analysis and global event tab.
- Phase 5 adds backtesting and live strategy scorecards.
- Phase 6 adds React Native mobile app and push notifications.
