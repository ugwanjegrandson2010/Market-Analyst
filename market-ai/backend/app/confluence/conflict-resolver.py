class ConflictResolver:

    def resolve(
            self,
            bullish,
            bearish
    ):
        if bullish > bearish:

            return "Bullish"
        elif bearish > bullish:

            return "Bearish"
        return "Neutral"
    