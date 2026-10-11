import pandas as pd
from .base_indicator import BaseIndicator


class ADX(BaseIndicator):
    def calculate(self, df):
        high = df["high"]; low = df["low"]; close = df["close"]
        prev_close = close.shift(1)
        tr = pd.concat([high-low, (high-prev_close).abs(), (low-prev_close).abs()], axis=1).max(axis=1)
        plus_dm = ((high - high.shift(1)).clip(lower=0))
        minus_dm = ((low.shift(1) - low).clip(lower=0))
        # zero out the smaller
        plus_dm = plus_dm.where(plus_dm > minus_dm, 0)
        minus_dm = minus_dm.where(minus_dm > plus_dm, 0)  # note: approximate
        tr14 = tr.rolling(14).sum()
        plus_di = 100 * (plus_dm.rolling(14).sum() / tr14)
        minus_di = 100 * (minus_dm.rolling(14).sum() / tr14)
        dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
        df["ADX_14"] = dx.rolling(14).mean()
        df["DMP_14"] = plus_di
        df["DMN_14"] = minus_di
        return df
