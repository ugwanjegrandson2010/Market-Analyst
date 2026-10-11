import pandas as pd
from .base_indicator import BaseIndicator


class Stochastic(BaseIndicator):
    def calculate(self, df):
        low14 = df["low"].rolling(14).min()
        high14 = df["high"].rolling(14).max()
        k = 100 * (df["close"] - low14) / (high14 - low14)
        df["STOCHk_14_3_3"] = k
        df["STOCHd_14_3_3"] = k.rolling(3).mean()
        return df
