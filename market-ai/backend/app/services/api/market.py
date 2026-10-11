from fastapi import APIRouter

from app.services.market_data import MarketDataEngine
from app.services.analysis import AnalysisEngine
from app.services.harvest import HarvestEngine

router = APIRouter()

engine = MarketDataEngine()
analyzer = AnalysisEngine()
harvester = HarvestEngine()

@router.get("/harvest/all")
def harvest_all():
    return harvester.harvest_all()

@router.get("/retrain")
def retrain():
    from app.services.reinforcement import ReinforcementEngine
    return ReinforcementEngine().retrain()

@router.get("/harvest/{symbol}")
def harvest(symbol: str):
    return harvester.harvest(symbol)

@router.get("/analyze/{symbol}")
def analyze(symbol: str):
    return analyzer.analyze(symbol, engine.get_history(symbol))

@router.get("/market/{symbol}")
def history(symbol: str):
    return engine.get_history(symbol)


@router.get("/analyze/{symbol}")
def analyze(symbol: str):
    rows = engine.get_history(symbol)
    return analyzer.analyze(symbol, rows)
