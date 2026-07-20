import pandas_ta as ta 
from .base_indicator import BaseIndicator

class RSI(BaseIndicator):
    def calculate(self, df): 

        df["RSI"] = ta.rsi(
            df["close"],
            length=14
        )
        return df 
    
    