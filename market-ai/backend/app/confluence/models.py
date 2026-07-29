from dataclasses import dataclass

@dataclass
class ConfluenceResult:

    direction: str
    score: float
    confidence: float 
    bullish_score: float
    bearish_score: float 
    reasons: list
    