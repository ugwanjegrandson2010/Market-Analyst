import urllib.request, json, re, html, time


CURATED_UNIVERSE = (
    ["AAPL","MSFT","NVDA","AMZN","GOOGL","META","TSLA","BRK-B","JPM","V","JNJ","WMT","XOM","PG","UNH",
     "HD","CVX","MA","BAC","ABBV","KO","PEP","PFE","MRK","COST","TMO","CSCO","AVGO","MCD","ACN"] +
    ["BTC-USD","ETH-USD","SOL-USD","XRP-USD","ADA-USD","DOGE-USD","AVAX-USD","DOT-USD","LINK-USD","MATIC-USD"] +
    ["EURUSD=X","GBPUSD=X","USDJPY=X","AUDUSD=X","USDCAD=X","USDCHF=X"] +
    ["GC=F","SI=F","CL=F","NG=F","HG=F","ZC=F","ZS=F"]
)


class HarvestEngine:
    def _fetch_json(self, url):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as r:
                return json.loads(r.read().decode())
        except Exception:
            return None

    def _fetch_text(self, url):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as r:
                return r.read().decode(errors="ignore")
        except Exception:
            return ""

    def _quote(self, symbol):
        data = self._fetch_json(f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}")
        if not data or "quoteResponse" not in data:
            return None
        res = data["quoteResponse"].get("result") or []
        if not res:
            return None
        q = res[0]
        return {
            "symbol": q.get("symbol"), "price": q.get("regularMarketPrice"),
            "change": q.get("regularMarketChange"), "changePercent": q.get("regularMarketChangePercent"),
            "volume": q.get("regularMarketVolume"), "marketCap": q.get("marketCap"),
            "currency": q.get("currency"), "exchange": q.get("fullExchangeName"),
        }

    def _news_tokens(self, symbol, limit=5):
        rss = self._fetch_text(f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US")
        titles = re.findall(r"<title>(.*?)</title>", rss, re.S)
        headlines = [html.unescape(t.strip()) for t in titles[1:limit+1]]
        tokens = []
        for h in headlines:
            for w in re.findall(r"[A-Za-z0-9$%\.]+", h.lower()):
                if len(w) > 2:
                    tokens.append(w)
        counts = {}
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1
        return headlines, tokens, counts

    def harvest(self, symbol: str):
        out = {"symbol": symbol, "sources": []}
        q = self._quote(symbol)
        if q:
            out["quote"] = q
        headlines, tokens, counts = self._news_tokens(symbol)
        out["headlines"] = headlines
        out["tokens"] = tokens
        out["token_counts"] = counts
        cg_map = {"BTC":"bitcoin","ETH":"ethereum","SOL":"solana","XRP":"ripple","ADA":"cardano","DOGE":"dogecoin"}
        base = symbol.split("-")[0].upper()
        if base in cg_map:
            cg = self._fetch_json(f"https://api.coingecko.com/api/v3/simple/price?ids={cg_map[base]}&vs_currencies=usd&include_24hr_change=true")
            if cg and cg_map[base] in cg:
                out["sources"].append({"name": "CoinGecko", "data": cg[cg_map[base]]})
        return out

    def harvest_many(self, symbols):
        results = []
        for s in symbols:
            r = self.harvest(s)
            results.append({
                "symbol": s,
                "price": r.get("quote", {}).get("price"),
                "changePercent": r.get("quote", {}).get("changePercent"),
                "volume": r.get("quote", {}).get("volume"),
                "top_tokens": list(r.get("token_counts", {}).items())[:5],
            })
            time.sleep(0.15)
        return results

    def harvest_all(self):
        return {"universe_size": len(CURATED_UNIVERSE), "results": self.harvest_many(CURATED_UNIVERSE)}
