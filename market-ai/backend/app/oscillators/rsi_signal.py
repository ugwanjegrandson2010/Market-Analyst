from .signal import TradingSignal
class RSISignal:
    def evaluate(self, df):
        value = df["RSI"].iloc[-1]
        if value < 30:

            return TradingSignal(
                "RSI",
                "Bullish",
                0.90,
                0.88,
                "RSI indicates oversold conditions."
            )
        if value > 70:
            return TradingSignal(
                "RSI",
                "Bearish",
                0.90,
                0.88,
                "RSI indicates overbought conditions."
            )
        
        return TradingSignal(
            "RSI",
            "Neutral",
            0.30,
            0.50,
            "RSI is within normal operating range."
        )