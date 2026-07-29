class SwingDetector:

    def detect(self, df, lookback=3):

        highs = []
        lows = []

        for i in range(lookback, len(df)-lookback):
            if df.high.iloc[i] == max(df.high.iloc[
                i-lookback: i+lookback+1
            ]

        ):
                highs.append(i)

                if df.low.iloc[i]  == min(

                    df.low.iloc[
                        i-lookback: i+lookback+1

                    ]
                ):

                    lows.append(i)

            return highs, lows
        