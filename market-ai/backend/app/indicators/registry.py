from .ema import EMA
from .sma import SMA
from .rsi import RSI 
from .macd import MACD 
from .bollinger import BollingerBands
from .atr import ATR 
from .adx import ADX
from .stochastic import Stochastic
from .vwap import VWAP

INDICATORS = [
    EMA(),
    SMA(),
    RSI(),
    MACD(),
    BollingerBands(),
    ATR(),
    ADX(),
    Stochastic(),
    VWAP()
]

