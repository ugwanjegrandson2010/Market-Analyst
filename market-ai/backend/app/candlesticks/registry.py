from .doji import Doji 
from .hammer import Hammer
from .shooting_star import ShootingStar
from .bullish_engulfing import BullishEngulfing
from .bearish_engulfing import BearishEngulfing
from .morning_star import MorningStar
from .evening_star import EveningStar

PATTERNS =[
    Doji(),

    Hammer(),

    ShootingStar(),

    BullishEngulfing(),

    BearishEngulfing(),

    MorningStar(),
    
    EveningStar()
]
