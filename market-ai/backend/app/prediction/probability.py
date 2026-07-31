class ProbabilityCalculator:
    def calculate(
            self,
            probabilities
    ):
        up = float(probabilities[0][1])
        down = float(probabilities[0][0])
        return up, down

        