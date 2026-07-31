from .feature_builder import FeatureBuilder
from .preprocessing import DataPreprocessor 
from .predictor import Predictor 

class InferencePipeline:

    def __init__(
            self,
            model_path

        ):

        self.builder = FeatureBuilder()
        self.scaler = DataPreprocessor()
        self.predictor = Predictor(
            model_path
        )

    def run(
            self,
            dataframe
    ):

        features = self.builder.build(
            dataframe
        )

        latest = features.tail(1)
        latest = self.scaler.fit_transform(
            latest
        )

        prediction = self.predictor.predict(
            latest
        )

        probabilities = self.predictor.predict_proba(
            latest
        )

        return prediction, probabilities

    

        
        