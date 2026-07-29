class SupportResistance:

    def detect(self, df):

        support = df.low.tail(50).min()

        resistance = df.high.tail(50).max()

        return{

            "support": support,

            "resistance": resistance
        }
    