def body_size(candle):

    return abs(
        candle["close"] -
        candle["open"]
    )


def upper_shadow(candle):

    return candle["high"] - max(
        candle["open"],
        candle["close"]
    )

def lower_shadow(candle):

    return min(
        candle["open"],
        candle["close"]
        )    - candle["low"]


    