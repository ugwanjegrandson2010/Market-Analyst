import pandas as pd
from .base_indicator import BaseIndicator


class MACD(BaseIndicator):
    def calculate(self, df):
        close = df["close"]
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        df["MACD_12_26_9"] = macd
        df["MACDs_12_26_9"] = signal
        df["MACDh_12_26_9"] = macd - signal
        return df
