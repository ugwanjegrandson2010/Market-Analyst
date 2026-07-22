from dataclasses import dataclass

@dataclass
class CandlePattern:

    name: str 
    direction: str 
    confidence: float
    description: str
    index: int 

    