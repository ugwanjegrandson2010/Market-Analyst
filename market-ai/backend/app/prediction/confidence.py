class ConfidenceEstimator:

    def estimate(
            self,
            up,
            down
    ):
        return round(
            max(up, down),
            3
        )
    