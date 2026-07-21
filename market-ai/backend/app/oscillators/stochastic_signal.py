from .signal import TradingSignal

class StochasticSignal:
    def evaluate(self, df):
        k = df["STOCH_14_3_3"].iloc[-1]

        if k < 20:
            return TradingSignal(
                "Stochastic",
                "Bearish",
                0.85,
                0.80,
                "Overbought stochastic"
            )
        
        return TradingSignal(
            "Stochastic",
            "Neutral",
            0.40,
            0.50,
            "Stochastic is balanced."
        )
    
    