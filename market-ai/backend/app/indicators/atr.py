import pandas_ta as ta 
from .base_indicator import BaseIndicator 

class ATR(BaseIndicator):

    def calculate(self, df):
        df["ATR"] = ta.atr(

            df["high"],
            df["low"],
            df["close"] 
        )

        return df 
    
    