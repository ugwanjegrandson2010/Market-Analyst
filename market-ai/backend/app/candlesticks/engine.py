from .registry import PATTERNS

class CandlestickEngine:
    def detect(self, df):

        results = []

        for detector in PATTERNS:

            pattern = detector.detect(df)
            if pattern:
                results.append(pattern)

                return results
            
            