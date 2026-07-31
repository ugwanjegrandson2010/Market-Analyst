from sklearn.preprocessing import StandardScaler

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()

    def fit_transform(self, x):
        return self.scaler.fit_transform(x)
    def transform(self, x):
        return self.scaler.transform(x)
    