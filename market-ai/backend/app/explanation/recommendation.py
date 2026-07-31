class RecommendationEngine:
    def generate(
            self, 
            direction,
            confidence
    ):
        if direction == "Bulllish":
            if confidence > 0.80:
                return "Strong Buy Bias"
            return "Buy Bias"
        if direction == "Bearish":
            if confidence > 0.80:
                return "Strong Sell Bias"
            return "Sell Bias"
        return "Wait For Confirmation"

    