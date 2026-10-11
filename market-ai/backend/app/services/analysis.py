from typing import List, Dict, Any
from app.confluence.engine import ConfluenceEngine
from app.confluence.models import ConfluenceResult
from types import SimpleNamespace


def _sma(values, period):
    if len(values) < period:
        return None
    return sum(values[-period:]) / period

def _ema(values, period):
    if len(values) < period:
        return None
    k = 2.0 / (period + 1)
    ema = values[0]
    for v in values[1:]:
        ema = v * k + ema * (1 - k)
    return ema

def _rsi(closes, period=14):
    if len(closes) < period + 1:
        return None
    gains = []
    losses = []
    for i in range(1, period + 1):
        d = closes[-(period + 1) + i] - closes[-(period + 1) + i - 1] if False else closes[i] - closes[i-1]
    # simpler: use last period+1
    seg = closes[-(period + 1):]
    gains = [max(seg[i]-seg[i-1], 0) for i in range(1, len(seg))]
    losses = [max(seg[i-1]-seg[i], 0) for i in range(1, len(seg))]
    avg_gain = sum(gains)/period
    avg_loss = sum(losses)/period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain/avg_loss
    return 100 - (100/(1+rs))

def _macd(closes):
    if len(closes) < 26:
        return None, None, None
    ema12 = _ema(closes, 12)
    ema26 = _ema(closes, 26)
    macd = ema12 - ema26 if (ema12 is not None and ema26 is not None) else None
    # signal from last 9 macds approximated
    signal = macd
    return macd, signal, (macd-signal) if signal is not None else None


class AnalysisEngine:
    def analyze(self, symbol: str, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not rows:
            return {"symbol": symbol, "error": "no data"}
        closes = [r["close"] for r in rows]
        latest = rows[-1]
        sma20 = _sma(closes, 20)
        sma50 = _sma(closes, 50)
        rsi = _rsi(closes, 14)
        macd, signal, hist = _macd(closes)

        signals = []
        trend_dir = "Bullish" if (sma50 is not None and closes[-1] > sma50) else "Bearish"
        conf = 0.65 if sma50 is not None else 0.5
        signals.append(SimpleNamespace(indicator="Trend", type="Trend", direction=trend_dir,
                                      confidence=conf, description=f"Price vs SMA50 ({'above' if trend_dir=='Bullish' else 'below'})"))

        if rsi is not None:
            if rsi > 70:
                d, c, desc = "Bearish", 0.6, f"RSI overbought ({rsi:.1f})"
            elif rsi < 30:
                d, c, desc = "Bullish", 0.6, f"RSI oversold ({rsi:.1f})"
            else:
                d, c, desc = ("Bullish" if rsi >= 50 else "Bearish"), 0.5, f"RSI neutral ({rsi:.1f})"
            signals.append(SimpleNamespace(indicator="RSI", type="RSI", direction=d, confidence=c, description=desc))

        if macd is not None:
            d = "Bullish" if macd >= 0 else "Bearish"
            signals.append(SimpleNamespace(indicator="MACD", type="MACD", direction=d,
                                          confidence=0.6, description=f"MACD {macd:.2f} (signal {signal:.2f})"))

        engine = ConfluenceEngine()
        fusion_bullish = 0.0
        fusion_bearish = 0.0
        reasons = []
        try:
            result = engine.evaluate(signals)
            summary = result  # placeholder
        except Exception:
            result = None
            summary = {}
        from app.confluence.summary import SummaryBuilder
        if result is not None:
            summary = SummaryBuilder().build(result.direction, result.confidence, result.reasons)

        # heuristic prediction (no ML deps)
        prob_up = 0.5
        if trend_dir == "Bullish": prob_up += 0.1
        if rsi is not None and rsi < 40: prob_up += 0.1
        if rsi is not None and rsi > 60: prob_up -= 0.1
        if macd is not None and macd > 0: prob_up += 0.1
        prob_up = max(0.05, min(0.95, prob_up))

        indicators = {
            "sma20": sma20, "sma50": sma50,
            "ema12": _ema(closes, 12), "ema26": _ema(closes, 26),
            "rsi14": rsi, "macd": macd, "macd_signal": signal,
            "latest_close": closes[-1],
        }

        return {
            "symbol": symbol,
            "latest": latest,
            "indicators": indicators,
            "signals": [{"indicator": s.indicator, "direction": s.direction,
                        "confidence": s.confidence, "description": s.description} for s in signals],
            "confluence": summary if isinstance(summary, dict) else (summary or {}),
            "prediction": {"direction": "up" if prob_up >= 0.5 else "down",
                           "probability_up": round(prob_up, 3),
                           "note": "heuristic; not financial advice"},
            "disclaimer": "Educational only. Not financial advice.",
        }
