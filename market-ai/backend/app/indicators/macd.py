import pandas_ta as ta 
from .base_indicator import BaseIndicator

class MACD(BaseIndicator):
     def calculate(self,df):
          
          macd = ta.macd(df["close"])

          df = df.join()
          return df 
     