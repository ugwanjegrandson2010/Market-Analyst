class SummaryBuilder:

    def build(
            self,
            direction,
            confidence,
            reasons
    ):
        return{
            "market_bias": direction,

            "confidence": confidence,

            "reasons": reasons

        }

    