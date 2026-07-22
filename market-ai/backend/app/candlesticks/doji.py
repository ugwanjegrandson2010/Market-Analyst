from .pattern import CandlePattern
from .base_pattern import BasePattern

class Doji(BasePattern):
    def detect(self, df):

        candle = df.iloc[-1]
        body = abs(
            candle.close -
            candle.open
        )

        if body < (
            candle.high -
            candle.low
        ) * 0.1:
            
            return CandlePattern(
                "Doji",
                "Neutral",
                0.85,
                "Market indesicion detected",
                len(df)-1
            )
        
        return None
    
    