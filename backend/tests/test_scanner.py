from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_reports_today_stocks() -> None:
    response = client.get("/reports/today?section=stocks")
    assert response.status_code == 200
    payload = response.json()
    assert payload["section"] == "stocks"
    assert isinstance(payload["reports"], list)
    assert len(payload["reports"]) > 0


def test_instrument_analysis_endpoint() -> None:
    response = client.get("/instruments/RELIANCE/analysis")
    assert response.status_code == 200
    payload = response.json()
    assert payload["symbol"] == "RELIANCE"
    assert 0 <= payload["score"] <= 100
