import random, math

class PureLogisticModel:
    def __init__(self, epochs=200, lr=0.05):
        self.epochs = epochs
        self.lr = lr
        self.w = None
        self.b = 0.0
        self.mean = None
        self.std = None

    def _standardize(self, X):
        if self.mean is None:
            n = len(X); d = len(X[0])
            self.mean = [sum(X[i][j] for i in range(n))/n for j in range(d)]
            self.std = [max(1e-9, (sum((X[i][j]-self.mean[j])**2 for i in range(n))/n)**0.5) for j in range(d)]
        return [[(x[j]-self.mean[j])/self.std[j] for j in range(len(x))] for x in X]

    def train(self, X, y):
        if not X or len(X) < 5: return False
        Xs = self._standardize(X)
        d = len(Xs[0])
        self.w = [0.0]*d
        self.b = 0.0
        for _ in range(self.epochs):
            gw = [0.0]*d; gb=0.0
            for i in range(len(Xs)):
                z = self.b + sum(self.w[j]*Xs[i][j] for j in range(d))
                p = 1/(1+math.exp(-z))
                err = p - y[i]
                for j in range(d): gw[j] += err*Xs[i][j]
                gb += err
            n=len(Xs)
            self.w = [self.w[j]-self.lr*gw[j]/n for j in range(d)]
            self.b -= self.lr*gb/n
        return True

    def _sigmoid(self, x):
        try:
            return 1/(1+math.exp(-x))
        except OverflowError:
            return 0.0 if x<0 else 1.0

    def predict_proba(self, x):
        if self.w is None: return 0.5
        xs = [(x[j]-self.mean[j])/self.std[j] for j in range(len(x))]
        z = self.b + sum(self.w[j]*xs[j] for j in range(len(xs)))
        return self._sigmoid(z)


class PredictionModel:
    def build_features(self, closes, indicators):
        feats = []
        # require at least 20 closes
        for i in range(20, len(closes)-1):
            c = closes[i]
            sma20 = sum(closes[i-19:i+1])/20.0
            # rsi approx using last slice
            seg = closes[i-13:i+1] if i>=13 else closes[:i+1]
            rsi = 50.0
            if len(seg)>1:
                gains=[max(seg[k]-seg[k-1],0) for k in range(1,len(seg))]
                losses=[max(seg[k-1]-seg[k],0) for k in range(1,len(seg))]
                ag=sum(gains)/len(gains) if gains else 0
                al=sum(losses)/len(losses) if losses else 1e-9
                rsi=100-(100/(1+ag/al)) if al>0 else 50
            macd = 0.0
            feats.append([c, sma20, rsi, macd])
        # targets: next close > current close
        targets = [1 if closes[i+1]>closes[i] else 0 for i in range(20, len(closes)-1)]
        return feats, targets

    def fit_predict(self, rows):
        closes=[r["close"] for r in rows]
        # last indicators snapshot passed separately; use rows only
        X,y = self.build_features(closes, None)
        model = PureLogisticModel()
        ok = model.train(X,y)
        if not ok or not X:
            return None
        # predict from last available feature row
        last_i = len(closes)-2
        if last_i < 20: return None
        # build single feature using last window
        i = last_i
        sma20 = sum(closes[i-19:i+1])/20.0
        seg = closes[i-13:i+1] if i>=13 else closes[:i+1]
        gains=[max(seg[k]-seg[k-1],0) for k in range(1,len(seg))]
        losses=[max(seg[k-1]-seg[k],0) for k in range(1,len(seg))]
        ag=sum(gains)/len(gains) if gains else 0
        al=sum(losses)/len(losses) if losses else 1e-9
        rsi=100-(100/(1+ag/al)) if al>0 else 50
        x=[closes[i], sma20, rsi, 0.0]
        prob = model.predict_proba(x)
        return {"probability_up": round(prob,3), "direction":"up" if prob>=0.5 else "down", "trained_samples":len(X)}
