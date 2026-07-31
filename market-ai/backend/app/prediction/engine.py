from .models import PredictionResult
from .inference import InferencePipeline
from .probability import ProbabilityCalculator
from .confidence import ConfidenceEstimator

class PredictionEngine:

    def __init__(
            self,
            model_path
    ):
        self.pipeline = InferencePipeline(
            model_path
        )

    def predict(
            self,
            dataframe
    ):
        prediction, probability = self.pipeline.run(
            dataframe
        )

        up, down = ProbabilityCalculator().calculate(

            probabilities
        ) 
        confidence = ConfidenceEstimator().estimate(
            up,
            down
        )

        direction = "Bullish" if up > down else "Bearish"
        return PredictionResult(
            direction = direction,
            probability_up = up,
            probability_down = down,
            confidence = confidence,
            expected_return = 0.0,
            model_name = "Random Forest",
            explanantion = "Prediction generated from the trained machine learning model."
        )
    