from .models import MarketStructureSignal

class TrendDetector:

    def detect(self, df):

        ema20 = df.EMA20.iloc[-1]
        ema50 = df.EMA50.iloc[-1]
        ema200 = df.EMA200.iloc[-1]

        if ema20 > ema50 > ema200:

            return MarketStructureSignal(
            "Trend",
            "Bullish",
            0.95,
            "Strong bullish trend."
        )

        if ema20 < ema50 < ema200:

            return MarketStructureSignal(
        "Trend",
        "Bearish",
        0.95,
        "Strong bearish trend."
    )
        return MarketStructureSignal(
    "Trend",
    "Sideways",
    0.60,
    "No dominant trend."
)
