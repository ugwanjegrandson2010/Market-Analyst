class ConfidenceCalculator:
    def calculate(
            self,
            bullish,
            bearish
    ):
        total = bullish + bearish 
        if total == 0:

            return 0 
        return round(
            max(
                bullish,
                bearish
            )/ total , 
            3
        )
    