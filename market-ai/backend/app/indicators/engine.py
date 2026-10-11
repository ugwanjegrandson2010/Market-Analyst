from .registry import INDICATORS

class IndicatorEngine:

    def run(self, dataframe):
         df = dataframe.copy()

         for indicator in INDICATORS:

              df = indicator.calculate(df)

         return df
         
         
