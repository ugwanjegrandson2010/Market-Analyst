from .models import MarketStructureSignal

class CHOCHDetector:

    def detect(self, df):

        ema20 = df.EMA20.iloc[-1]
        ema50 = df.EMA50.iloc[-1]

        previous20 = df.EMA20.iloc[-2]
        previous50 = df.EMA50.iloc[-2]
        if previous20 < previous50 and ema20 > ema50:
            return MarketStructureSignal(
                "CHOCH",
                "Bullish",
                0.85,
                "Bullish Change of Character."
            )

        if previous20 > previous50 and ema20 < ema50:
            return MarketStructureSignal(
                "CHOCH",
                "Bearish",
                0.85,
                "Bearish Change of Character."
            )
        return None
     
    