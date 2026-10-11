from typing import Dict, Any


class RiskEngine:
    def analyze(self, symbol: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        ind = analysis.get("indicators", {})
        pred = analysis.get("prediction", {})
        entry = ind.get("latest_close", 0.0)
        atr_proxy = max(0.5, (ind.get("sma20") or entry) - (ind.get("sma50") or entry) * 0.0)
        stop_distance = max(entry * 0.01, abs((ind.get("sma50") or entry) - entry) * 0.5 if ind.get("sma50") else entry * 0.01)
        is_buy = pred.get("direction") == "up"
        if is_buy:
            stop_loss = round(entry - stop_distance, 4)
            take_profit = round(entry + (stop_distance * 3), 4)
        else:
            stop_loss = round(entry + stop_distance, 4)
            take_profit = round(entry - (stop_distance * 3), 4)
        risk = round(stop_distance, 4)
        reward = round(stop_distance * 3, 4)
        rr = round(reward / risk, 2) if risk else 0.0
        balance = 10000.0
        risk_pct = 0.01
        risk_amount = balance * risk_pct
        position_size = round(risk_amount / risk, 4) if risk else 0.0
        conf = analysis.get("confluence", {}).get("confidence", 0.5)
        prob = pred.get("probability_up", 0.5)
        quality = round((conf * 0.4 + prob * 0.4 + min(rr / 3, 1) * 0.2), 3)
        approved = quality >= 0.55 and rr >= 1.5
        decision = "APPROVED" if approved else "REJECTED"
        return {
            "symbol": symbol,
            "entry_price": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk": risk,
            "reward": reward,
            "risk_reward_ratio": rr,
            "balance": balance,
            "risk_amount": round(risk_amount, 2),
            "position_size": position_size,
            "trade_quality": quality,
            "decision": decision,
            "reasons": [
                f"Confluence confidence {conf:.2f}",
                f"Prediction probability {prob:.2f}",
                f"Risk/Reward {rr:.2f}",
            ],
            "note": "Educational only. Not financial advice.",
        }
