class ReasonBuilder:

    def build(self, signals):

        reasons = []

        for signal in signals:

            if hasattr(signal, "description"):

                reasons.append(signal.description)

            elif hasattr(signal, "reason"):
                reasons.append(signal.reason)

        return reasons 
    