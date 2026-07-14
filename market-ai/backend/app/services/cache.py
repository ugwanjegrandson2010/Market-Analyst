class MarketCache:
    def __init__(self):
        self.cache = {}

    def save(self, symbol, candles):
        self.cache[symbol] = candles

    def load(self, symbol):
        return self.cache.get(symbol, [])
