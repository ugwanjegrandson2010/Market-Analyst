import pandas_ta as ta
from .base_indicator import BaseIndicator

class EMA(BaseIndicator):

    def calculate(self, df):

        df["EMA20"] = ta.ema(
            df["close"],
            length=20
        )

        df["EMA50"] = ta.ema(
            df["close"],
            length=50
        )
        return df
    