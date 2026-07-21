from .signal import TradingSignal 

class EMASignal:

    def evaluate(self, df):

        price = df["close"].iloc[-1]

        ema20 = df["EMA20"].iloc[-1]
        
        ema30 = df["EMA30"].iloc[-1]

        ema50 = df["EMA50"].iloc[-1]

        ema200 = df["EMA200"].iloc[-1]
        if price > ema20 > ema50 > ema200:

            return TradingSignal(
                
            )