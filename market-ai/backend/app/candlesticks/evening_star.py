from .pattern import CandlePattern
from .base_pattern import BasePattern

class EveningStar(BasePattern):

    def detect(self, df):

        if len(df) < 3:
            return None
        
        a, b, c = df.iloc[-3:]

        if (
            a.close > a.open and
            abs(b.close - b.open) < abs(a.close - a.open) * 0.3 and 
            c.close < c.open
        ):
            
            return CandlePattern(
                "Evening Star",
                "Bearish",
                0.95,
                "Three-candle bearish reversal.",
                len(df)-1
            )
        
        return None
    