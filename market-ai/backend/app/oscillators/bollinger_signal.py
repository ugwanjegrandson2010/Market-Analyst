from .signal import TradingSignal

class BollingerSignal:

    def evaluate(self, df):
        price = df["close"].iloc[-1]
        upper = df["BBU_20_2.0"].iloc[-1]
        lower = df["BBL"]