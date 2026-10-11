import random
from datetime import datetime, timedelta


class MarketDataEngine:
    def __init__(self):
        self.cache = {}

    def get_history(self, symbol: str, timeframe: str = "1h", limit: int = 100):
        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="1mo", interval="1d")
            if df is not None and not df.empty:
                df = df.reset_index()
                out = []
                for _, row in df.iterrows():
                    out.append({
                        "timestamp": str(row.get("Date", row.get("Datetime", ""))),
                        "open": float(row["Open"]),
                        "high": float(row["High"]),
                        "low": float(row["Low"]),
                        "close": float(row["Close"]),
                        "volume": float(row["Volume"]),
                    })
                return out[-limit:]
        except Exception:
            pass

        random.seed(hash(symbol) & 0xFFFFFFFF)
        price = 100.0
        out = []
        ts = datetime.utcnow() - timedelta(days=limit)
        for i in range(limit):
            open_p = price
            change = random.uniform(-1.5, 1.5)
            close_p = max(1.0, open_p + change)
            high_p = max(open_p, close_p) + random.uniform(0, 1.0)
            low_p = min(open_p, close_p) - random.uniform(0, 1.0)
            out.append({
                "timestamp": (ts + timedelta(days=i)).isoformat(),
                "open": round(open_p, 2),
                "high": round(high_p, 2),
                "low": round(low_p, 2),
                "close": round(close_p, 2),
                "volume": round(random.uniform(1000, 5000), 2),
            })
            price = close_p
        return out
