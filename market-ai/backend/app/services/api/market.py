from fastapi import APIRouter

from app.services.market_data MarketDataEngine

router = APIRouter()

engine = MarketDataEngine()

@router.get("/market/{symbol}")

def history(symbol: str):

    return engine.get_history(symbol)
