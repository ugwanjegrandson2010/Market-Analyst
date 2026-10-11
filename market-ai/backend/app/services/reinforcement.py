import sqlite3, json, time, os, math

DB_PATH = "data/reinforce.db"
WEIGHTS_PATH = "data/model_weights.json"

class ReinforcementEngine:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._ensure()

    def _ensure(self):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT, ts REAL, close REAL, features TEXT,
            prob REAL, direction TEXT, actual_up INTEGER, updated REAL
        )""")
        self.conn.commit()

    def log_prediction(self, symbol, features, prob, direction, close):
        self.conn.execute(
            "INSERT INTO observations(symbol,ts,close,features,prob,direction,actual_up,updated) VALUES (?,?,?,?,?,?,NULL,?)",
            (symbol, time.time(), close, json.dumps(features), prob, direction, time.time()))
        self.conn.commit()
        # label prior pending observation if exists
        self._update_outcome(symbol, close)

    def _update_outcome(self, symbol, close):
        cur = self.conn.execute(
            "SELECT id, close FROM observations WHERE symbol=? AND actual_up IS NULL ORDER BY id DESC LIMIT 1",
            (symbol,)).fetchone()
        # the most recent pending is the one we just inserted (actual_up NULL); skip it by taking second
        rows = self.conn.execute(
            "SELECT id, close FROM observations WHERE symbol=? AND actual_up IS NULL ORDER BY id DESC",
            (symbol,)).fetchall()
        # label all but the latest pending
        for oid, prev_close in rows[1:]:
            actual = 1 if close > prev_close else 0
            self.conn.execute("UPDATE observations SET actual_up=?, updated=? WHERE id=?",
                             (actual, time.time(), oid))
        self.conn.commit()

    def labeled_count(self):
        return self.conn.execute("SELECT COUNT(*) FROM observations WHERE actual_up IS NOT NULL").fetchone()[0]

    def retrain(self):
        rows = self.conn.execute(
            "SELECT features, actual_up FROM observations WHERE actual_up IS NOT NULL").fetchall()
        if len(rows) < 5:
            return {"status": "insufficient_labels", "labeled": len(rows)}
        X = [json.loads(r[0]) for r in rows]
        y = [r[1] for r in rows]
        # standardize
        d = len(X[0])
        means = [sum(X[i][j] for i in range(len(X)))/len(X) for j in range(d)]
        stds = [max(1e-9, (sum((X[i][j]-means[j])**2 for i in range(len(X)))/len(X))**0.5) for j in range(d)]
        Xs = [[(X[i][j]-means[j])/stds[j] for j in range(d)] for i in range(len(X))]
        w = [0.0]*d; b=0.0
        lr=0.05
        for _ in range(500):
            gw=[0.0]*d; gb=0.0
            for i in range(len(Xs)):
                z=b+sum(w[j]*Xs[i][j] for j in range(d))
                p=1/(1+math.exp(-z))
                err=p-y[i]
                for j in range(d): gw[j]+=err*Xs[i][j]
                gb+=err
            n=len(Xs)
            w=[w[j]-lr*gw[j]/n for j in range(d)]
            b-=lr*gb/n
        payload={"weights":w,"bias":b,"means":means,"stds":stds,"trained_samples":len(X)}
        with open(WEIGHTS_PATH,"w") as f:
            json.dump(payload, f)
        return {"status":"ok","trained_samples":len(X)}

    def predict(self, features):
        if not os.path.exists(WEIGHTS_PATH):
            return None
        with open(WEIGHTS_PATH) as f:
            p=json.load(f)
        w=p["weights"]; b=p["bias"]; means=p["means"]; stds=p["stds"]
        xs=[(features[j]-means[j])/stds[j] for j in range(len(features))]
        z=b+sum(w[j]*xs[j] for j in range(len(xs)))
        prob=1/(1+math.exp(-z))
        return {"direction":"up" if prob>=0.5 else "down","probability_up":round(prob,3),
                "trained_samples":p["trained_samples"],"source":"reinforced_model"}
