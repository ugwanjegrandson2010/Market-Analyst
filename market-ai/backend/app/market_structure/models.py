from dataclasses import dataclass 

@dataclass
class MarketStructureSignal:

    type: str
    direction: str
    confidence: float
    description: str
    

  