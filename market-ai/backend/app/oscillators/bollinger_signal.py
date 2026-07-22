from .signal import TradingSignal

class BollingerSignal:

    def evaluate(self, df):
        price = df["close"].iloc[-1]
        upper = df["BBU_20_2.0"].iloc[-1]
        lower = df["BBL_20_2.0"].iloc[-1]

        if price < lower:

            return TradingSignal(
                "Bollinger",
                "Bullish",
                0.75,
                0.78,
                "Price below lower Bollinger Band."
            )
        
        if price > upper:

            return TradingSignal(
                "Bollinger",
                "Bearish",
                0.75,
                0.78,
                "Price above upper Bollinger Band."
            )
        
        return TradingSignal(
            "Bollinger",
            "Neutral",
            0.40,
            0.55,
            "Price within Bollinger Bands."
        )
    