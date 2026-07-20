import pandas_ta as ta 
from .base_indicator import BaseIndicator 

class ADX(BaseIndicator):
  def calculate(self, df):

    adx = ta.adx(
        df["high"],
        df["low"],
        df["close"]
    )

    df = df.join(adx)
    return df 
