from .weights import WEIGHTS

class SignalFusion:

    def combine(self, signals):

        bullish = 0 

        bearish = 0 

        reasons = []
        for signal in signals:

            weight = WEIGHTS.get(
            signal.indicator if hasattr(signal, "indicator")
            else signal.type,
            5
        )
        if signal.direction == "Bullish":
            bullish += weight * signal.confidence

        elif signal.direction == "Bearish":
            bearish += weight * signal.confidence

        reasons.append(signal.description if hasattr(signal, "description") else signal.reason)

        return bullish, bearish, reasons