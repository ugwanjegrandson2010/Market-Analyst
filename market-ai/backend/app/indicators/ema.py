import pandas as pd
from .base_indicator import BaseIndicator


class EMA(BaseIndicator):
    def calculate(self, df):
        df["EMA20"] = df["close"].ewm(span=20, adjust=False).mean()
        df["EMA50"] = df["close"].ewm(span=50, adjust=False).mean()
        return df
