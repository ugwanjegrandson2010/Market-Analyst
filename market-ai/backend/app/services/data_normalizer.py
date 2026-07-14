class DataNormalizer:
    def __init__(self):
        pass

    @staticmethod
    def normalize(candle):
        candle.open = float(candle.open)
        candle.high = float(candle.high)
        candle.low = float(candle.low)
        candle.close = float(candle.close)
        candle.volume = float(candle.volume)

        return candle
