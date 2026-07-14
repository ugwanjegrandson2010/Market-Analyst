from app.services.binance_provider import BinanceProvider
from app.services.data_validator import DataValidator
from app.services.data_normalizer import DatNormalizer
from app.services.cache import MarketCache


class MarketDataService:
    def __init__(self):
        self.provider = BinanceProvider()

        self.cache = MarketCache()

        def get_history(
                self,
                symbol,
                timefrrame = '1h'
            
        ):
            candles = self.provider.fetch_ohlcv(
                symbol,
                timeframe
            )
        clean = []

        for row in candles: 

            candle = {
                "timestamp" : row[0],
                "open" : row[1],
                "high" : row[2],
                "close" : row[4],
                "volume" : row[5]
            }

candle = DataNormalizer.normalize(candle)

if DataValidator.validate(candle):

    clean.append(candle)

    self.cache.save(symbol, clean)


return clean


class MarketDataService:
    def connect(self):
        pass
    def fetch(self):
        pass
    def stream(self):
        pass
    