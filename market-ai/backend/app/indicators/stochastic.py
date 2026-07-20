import pandas_ta as ta 
from .base_indicator import BaseIndicator 

class Stochastic(BaseIndicator):

    def calculate(self, df):
        stoch = ta.stoch(
            df["high"],
            df["low"],
            df["close"]
        )

        df = df.join(stoch)

        return df 
       