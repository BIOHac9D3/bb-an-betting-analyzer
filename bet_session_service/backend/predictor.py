import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

_model_path = "model.joblib"
_encoder_path = "encoder.joblib"
_model = None
_encoder = LabelEncoder()

def train_model(bets):
    df = pd.DataFrame(bets)
    df = df.dropna(subset=["amount", "payout", "game"])
    df["target"] = df["payout"].apply(lambda x: 1 if x > 0 else 0)
    df["game_enc"] = _encoder.fit_transform(df["game"])
    X = df[["amount", "game_enc"]]
    y = df["target"]

    global _model
    _model = RandomForestClassifier(n_estimators=100)
    _model.fit(X, y)

    joblib.dump(_model, _model_path)
    joblib.dump(_encoder, _encoder_path)

    y_pred = _model.predict(X)
    report = classification_report(y, y_pred, output_dict=True)
    matrix = confusion_matrix(y, y_pred).tolist()
    return {"report": report, "confusion_matrix": matrix}

def predict_outcomes(bets):
    global _model, _encoder
    if _model is None and os.path.exists(_model_path):
        _model = joblib.load(_model_path)
        _encoder = joblib.load(_encoder_path)

    if _model is None:
        return [{"game": b["game"], "prediction": "Model not trained"} for b in bets]

    df = pd.DataFrame(bets)
    df["game_enc"] = _encoder.transform(df["game"])
    X = df[["amount", "game_enc"]]
    pred = _model.predict(X)
    return [
        {"game": row["game"], "amount": row["amount"], "prediction": "Win" if p else "Loss"}
        for row, p in zip(bets, pred)
    ]
