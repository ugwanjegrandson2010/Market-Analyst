import pandas as pd
import numpy as np
from .base_indicator import BaseIndicator


class ATR(BaseIndicator):
    def calculate(self, df):
        high = df["high"]; low = df["low"]; close = df["close"]
        prev_close = close.shift(1)
        tr = pd.concat([high-low, (high-prev_close).abs(), (low-prev_close).abs()], axis=1).max(axis=1)
        df["ATR"] = tr.rolling(14).mean()
        return df
