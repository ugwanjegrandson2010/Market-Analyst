from .signal import TradingSignal 
class MACDSignal:
    def evaluate(self, df):
        macd = df["MACD_12_26_9"].iloc[-1]

        signal = df["MACD_12_26_9"].iloc[-1]

        if macd > signal:
            return TradingSignal(
                "MACD",
                "Bullish",
                0.80,
                0.82,
                "Bullish MACD crossover"
            )
        if macd > signal:
            return TradingSignal(
                "MACD",
                "Bearish",
                0.80,

                0.82,
                "Bearish MACD crossover"
            )
        
        return TradingSignal(
            "MACD",
            "Neutral",
            0.50,
            0.50,
            "MACD signal line are aligned"
        )
    
    
    