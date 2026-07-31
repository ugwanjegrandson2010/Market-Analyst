from dataclasses import dataclass

@dataclass
class PredictionResult:
    direction: str 
    probability_up: float
    probability_down: float 
    confidence: float
    expected_return: float
    model_name: str 
    explanation: str
    