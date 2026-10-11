import pandas as pd
from .base_indicator import BaseIndicator


class VWAP(BaseIndicator):
    def calculate(self, df):
        tp = (df["high"] + df["low"] + df["close"]) / 3
        df["VWAP"] = (tp * df["volume"]).cumsum() / df["volume"].cumsum()
        return df
