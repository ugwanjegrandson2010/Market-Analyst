from .pattern import CandlePattern
from .base_pattern import BasePattern

class BullishEngulfing(BasePattern):

    def detect(self, df):

        if len(df) < 2:
            return None
        prev = df.iloc[-2]

        curr = df.iloc[-1]

        if (
            prev.close < prev.open and 
            curr.close > curr.open and 
            curr.open < prev.close and 
            curr.close > prev.open
        ):
            return CandlePattern(
                "Bullish Engulfing",
                "Bullish",
                0.93,
                "Bullish engulfing pattern confirmed.",
                len(df)-1
            )
        
        return None
    
    