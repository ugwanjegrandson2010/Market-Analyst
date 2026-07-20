from dataclasses import dataclass

@dataclass
class TradingSignal:
    indicator:str

    direction: str

    strength: float

    confidence: float
     
    reason: str
