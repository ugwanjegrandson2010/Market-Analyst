from .registry import MODULES
from .support_resistance import SupportResistance
from .swing_detector import SwingDetector

class MarketStructureEngine:

    def analyze(self, df):

        results = []
        swing = SwingDetector()

        highs, lows = swing.detect(df)

        results.append({
            "swing_high": highs,
            "swing_lows": lows
        })

        sr = SupportResistance()
        results.append(
            sr.detect(df)
        )
        for  detector in MODULES:
         signal = detector.detect(df)

        if signal:
           results.append(signal)

           return results

        
