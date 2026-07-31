import joblib 

class Predictor:

    def __init__(self, path):

        self.model = joblib.load(path)

    def predict(self, features):

        return self.model.preedict(features)

    def predict_proba(self, features):

        return self.model.predict_proba(features)

    
        