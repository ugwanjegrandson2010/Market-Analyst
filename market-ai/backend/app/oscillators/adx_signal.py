from .signal import TradingSignal

class ADXSignal:

    def evaluate(self, df):
        adx = df["ADX_14"].iloc[-1]

        if adx > 25:

            return TradingSignal(
                "ADX",
                "Strong Trend",
                0.90,
                0.90,
                "Trend strength exceeds threshold"
            )
        
        return TradingSignal(
            "ADX",
            "Weak Trend",
            0.40,
            0.60,
            "Trend lacks strenghth"
        )
    
