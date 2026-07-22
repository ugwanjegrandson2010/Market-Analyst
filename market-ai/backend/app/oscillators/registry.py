from .rsi_signal import RSISignal
from .macd_signal import MACDSignal
from .stochastic_signal import StochasticSignal
from .adx_signal import ADXSignal
from .ema_signal import EMASignal
from .bollinger_signal import BollingerSignal

SIGNAL = [
    RSISignal(),

    MACDSignal(),

    StochasticSignal(),

    ADXSignal(),

    EMASignal(),

    BollingerSignal()
]
