from .models import MarketStructureSignal

class BOSDetector:

    def detect(self, df):

        previous_high = df.high.iloc[-2]

        current_close = df.close.iloc[-1]

        if current_close > previous_high:
            return MarketStructureSignal(
                "Break of Structure",
                "Bullish",
                0.90,
                "Bullish BOS detected."
            )
        previous_low = df.low.iloc[-2]

        if current_close < previous_low:
            return MarketStructureSignal(
                "Break of Structure",
                "Bearish",
                0.90,
                "Bearish BOS detected."
            )
        return None 

    