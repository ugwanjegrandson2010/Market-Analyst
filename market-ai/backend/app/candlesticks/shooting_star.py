from .pattern import CandlePattern
from .base_pattern import BasePattern

class ShootingStar(BasePattern):
    def detect(self, df):

        candle = df.iloc[-1]
        body = abs(
            candle.close - 
            candle.open
        )

        upper = candle.high - max(
            candle.close,
            candle.open 
        )

        if upper > body * 2:

            return CandlePattern(
                "Shooting Star",
                "Bearish",
                0.88,
                "Potential bearish reversal",
                len(df)-1
            )
        
        return None
    