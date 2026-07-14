class DataValidator:
    @staticmethod
    def validate(candle):
        if candle.high < candle.low:
            return False
        if candle.open <= 0:
            return False
        if candle.close <= 0:
            return False

        return True
