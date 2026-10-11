import pandas as pd
from .base_indicator import BaseIndicator


class BollingerBands(BaseIndicator):
    def calculate(self, df):
        mid = df["close"].rolling(20).mean()
        std = df["close"].rolling(20).std()
        df["BBM_20_2.0"] = mid
        df["BBU_20_2.0"] = mid + 2 * std
        df["BBL_20_2.0"] = mid - 2 * std
        return df
