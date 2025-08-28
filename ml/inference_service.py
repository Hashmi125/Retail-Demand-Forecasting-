import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Retail Forecasting Inference")

# load trained model bundle
try:
    bundle = joblib.load("models/model.joblib")
    model = bundle["model"]
    feature_cols = bundle["feature_cols"]
except Exception as e:
    model = None
    feature_cols = None
    print("Model not found or failed to load:", e)

class ForecastRequest(BaseModel):
    product_id: int
    store_id: int
    dow: int
    is_holiday: int
    price: float
    lag_1: float
    lag_7: float
    roll7: float

@app.post("/forecast")
def forecast(req: ForecastRequest):
    if model is None or feature_cols is None:
        raise HTTPException(status_code=503, detail="Model not available. Train model first and ensure models/model.joblib exists.")

    row = pd.DataFrame([req.dict()])[feature_cols]
    # ensure dtypes
    row = row.astype(float)
    yhat = float(model.predict(row)[0])
    return {"predicted_units": max(0.0, round(yhat, 3))}

