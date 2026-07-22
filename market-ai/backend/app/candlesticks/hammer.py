from .pattern import CandlePattern 
from .base_pattern import BasePattern

class Hammer(BasePattern):

    def detect(self, df):
        candle = df.iloc[-1]

        body = abs(
            candle.close - 
            candle.open
        )

        lower = min(
            candle.open,
            candle.close
         ) - candle.low
        
        if lower > body * 2:

            return CandlePattern(
                "Hammer",
                "Bullish",
                0.88,
                "Potential bullish reversal",
                len(df)-1
            )
        
        return None
    