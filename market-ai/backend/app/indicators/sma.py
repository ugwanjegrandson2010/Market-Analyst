import pandas as pd
from .base_indicator import BaseIndicator


class SMA(BaseIndicator):
    def calculate(self, df):
        df["SMA20"] = df["close"].rolling(20).mean()
        df["SMA50"] = df["close"].rolling(50).mean()
        df["SMA200"] = df["close"].rolling(200).mean()
        return df
