from dataclasses import dataclass
from typing import List

@dataclass 
class AnalysisReport:
    title: str

    summary:str

    recommendation:str

    confidence:float

    reasons: List[str]
    risks: List[str]

    