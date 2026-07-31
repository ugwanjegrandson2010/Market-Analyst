from sklearn.ensemble import RandomForestClassifier
import joblib 

class Trainer:
    def train(
            self,
            x_train,
            y_train,
            output_file
    ):
        model = RandomForestClassifier(
            n_estimators=300,
            random_state=42
        )
        model.fit(
            x_train,
            y_train
        )
        joblib.dump(
            model,
            output_file
        )
        return model

    