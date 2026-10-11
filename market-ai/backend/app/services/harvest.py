import urllib.request, json, re, html


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

    def harvest(self, symbol: str):
        out = {"symbol": symbol, "sources": []}
        # CoinGecko simple price (crypto-oriented). Map common tickers.
        cg_symbol = symbol.lower()
        mapping = {"btc": "bitcoin", "eth": "ethereum", "sol": "solana", "ada": "cardano", "xrp": "ripple"}
        cg_id = mapping.get(cg_symbol, cg_symbol)
        cg = self._fetch_json(f"https://api.coingecko.com/api/v3/simple/price?ids={cg_id}&vs_currencies=usd&include_24hr_change=true")
        if cg and cg_id in cg:
            out["sources"].append({"name": "CoinGecko", "data": cg[cg_id]})
        # Yahoo Finance RSS headlines tokenized.
        rss = self._fetch_text(f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US")
        titles = re.findall(r"<title>(.*?)</title>", rss, re.S)
        headlines = [html.unescape(t.strip()) for t in titles[1:6]]  # skip feed title
        tokens = []
        for h in headlines:
            for w in re.findall(r"[A-Za-z0-9$%\.]+", h.lower()):
                if len(w) > 2: tokens.append(w)
        out["headlines"] = headlines
        out["tokens"] = tokens
        out["token_counts"] = {}
        for t in tokens:
            out["token_counts"][t] = out["token_counts"].get(t, 0) + 1
        return out
