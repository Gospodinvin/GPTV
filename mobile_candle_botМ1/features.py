
import numpy as np

def build_features(candles):
    X=[]
    for i in range(1,len(candles)):
        c=candles[i]
        body=abs(c["close"]-c["open"])
        direction=np.sign(c["close"]-c["open"])
        vol=c["high"]-c["low"]
        X.append([body,direction,vol])
    return np.array(X)
