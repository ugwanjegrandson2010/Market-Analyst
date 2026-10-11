from fastapi import APIRouter

from app.services.market_data import MarketDataEngine
from app.services.analysis import AnalysisEngine

router = APIRouter()

engine = MarketDataEngine()
analyzer = AnalysisEngine()


@router.get("/market/{symbol}")
def history(symbol: str):
    return engine.get_history(symbol)


@router.get("/analyze/{symbol}")
def analyze(symbol: str):
    rows = engine.get_history(symbol)
    return analyzer.analyze(symbol, rows)
