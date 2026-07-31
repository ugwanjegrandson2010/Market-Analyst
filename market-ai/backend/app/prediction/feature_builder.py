import pandas as pd 

class FeatureBuilder:

    FEATURES = [
        "close",
        "volume",
        "EMA20",
        "EMA50",
        "RSI",
        "ATR",
        "ADX_14",
        "MACD_12_26_9",
        "MACD_12-26_9"
    ]

    def build(self, dataframe):

        return dataframe[self.FEATURES].copy()

    