# Market Analyst (Market AI)

FastAPI backend for market data analysis, indicators, confluence scoring, harvesting, and risk assessment.

## Requirements

- Python 3.11
- Local virtual environment at `market-ai/backend/.venv`

## Setup

```bash
cd market-ai/backend
.venv/bin/uvicorn main:app --port 8000
```

API base URL: `http://127.0.0.1:8000`

Interactive docs: `http://127.0.0.1:8000/docs`

## Endpoints

- `GET /api/market/{symbol}` - Market history
- `GET /api/analyze/{symbol}` - Analysis for a symbol
- `GET /api/risk/analyze/{symbol}` - Risk assessment
- `GET /api/harvest/{symbol}` - Harvest data for one symbol
- `GET /api/harvest/all` - Harvest curated multi-asset universe
- `GET /api/retrain` - Retrain reinforcement model

## Notes

- Pure Python indicators; pandas/scikit-learn excluded due to CPU constraints.
- `.venv/` and `__pycache__/` are gitignored.
