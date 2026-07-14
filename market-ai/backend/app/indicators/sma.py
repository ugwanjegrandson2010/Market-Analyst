import pandas_ta as ta
from .base_indicator import BaseIndicator

class SMA(BaseIndicator):
    def calculate(self, df):

        df["SMA20"] = ta.sma(
            df["close"],
            0
        )

        df["SMA50"] = ta.sma(
            df["close"],
            50
        )

        df["SMA200"] = ta.sma(
            df["close"],
            200
        )
        return df