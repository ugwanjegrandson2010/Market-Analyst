from .pattern import CandlePattern
from .base_pattern import BasePattern

class MorningStar(BasePattern):

    def detect(self, df):

        if len(df) < 3:
            return None
        
        a, b, c = df.iloc[-3:]

        if (
            a.close < a.open and
            abs(b.close - b.open) < abs(a.close - a.open) * 0.3 and 
            c.close > c.open
        ):
            
            return CandlePattern(
                "Morning Star",\
                "Bullish",
                0.95,
                "Three-candle bullish reversal.",
                len(df)-1
            )
        return None
    