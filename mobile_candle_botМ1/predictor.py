
import numpy as np
from cv_extractor import extract_candles
from features import build_features
from model import CandleModel

model=CandleModel()

def analyze(image):
    candles=extract_candles(image)
    if len(candles)<12: return None
    X=build_features(candles)
    y=(X[:,1]>0).astype(int)
    model.fit(X[:-1],y[:-1])
    p=model.predict(X[-3:])[:,1].mean()
    return round(p,2)
