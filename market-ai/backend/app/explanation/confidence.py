class ConfidenceNarrator:

    def describe(
            self,
            confidence
    ):

        if confidence > 0.90:
            return "Very High"

        if confidence > 0.75:
            return "High"
        if confidence > 0.60:

            return "Moderate"

        return "Low"

    