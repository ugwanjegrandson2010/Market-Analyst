from templates import *

class SummaryGenerator:

    def build(self, direction):

        if direction == "Bullish":
            return BULLISH
        if direction == "Bearish":
            return BEARISH 

        return NEUTRAL

    