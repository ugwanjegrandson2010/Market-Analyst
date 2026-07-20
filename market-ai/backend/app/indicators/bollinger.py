import pandas_ta as ta 
from .base_indicator import BaseIndicator

class MollingerBands(BaseIndicator):
    def calculate(self,df):
        bb = ta.bbands(df["close"])

        df = df.join(bb)
        return df 
    
    