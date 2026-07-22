from .registry import SIGNAL

class OscillatorEngine:
    def evaluate(self, df):
        results = []

        for signal in SIGNAL:

            results.append(
                signal.evaluate(df)
            )

            return results
        
