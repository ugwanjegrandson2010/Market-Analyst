try:
    import ccxt
except ImportError:  # pragma: no cover - optional dependency
    ccxt = None


class BinanceProvider:
    def __init__(self):
        if ccxt is None:
            raise ImportError("ccxt is required to use BinanceProvider")
        self.exchange = ccxt.binance()

    def fetch_ohlcv(self, symbol, timeframe="1h", limit=500):
        return self.exchange.fetch_ohlcv(
            symbol,
            timeframe=timeframe,
            limit=limit,
        )

