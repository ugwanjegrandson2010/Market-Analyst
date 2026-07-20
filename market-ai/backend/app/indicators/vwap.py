import pandas_ta as ta 
from .base_indicator import BaseIndicator 

class VWAP(BaseIndicator):
    def calculate(self, df):
        df["VWAP"] = ta.vwap(
            df["high"],
            df["low"],
            df["close"],
            df["volume"]

        )

        return df 
    

    