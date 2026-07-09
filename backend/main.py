from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

app = FastAPI(title="Carbon-Smart-Charging-API")

# ==============================
# Load models
# ==============================
carbon_model = joblib.load("models/carbon_intensity_model.pkl")
cluster_model = joblib.load("models/customer_behavior_kmeans_model.joblib")
cluster_scaler = joblib.load("models/customer_behavior_scaler.joblib")


# ==============================
# Load historical carbon data
# ==============================
# CSV must contain: timestamp, ci_direct

BASE_DIR = Path(__file__).resolve().parent

carbon_history = pd.read_csv(
    BASE_DIR / "data/EV_Grid_Dataset.csv",
    parse_dates=["Datetime (UTC)"]
).sort_values("Datetime (UTC)")

carbon_history.set_index("Datetime (UTC)", inplace=True)

# ==============================
# Input Schemas
# ==============================

class CarbonRequest(BaseModel):
    timestamp: datetime   # ONLY INPUT


class UserClusterInput(BaseModel):
    arrival_hour: float
    charging_duration: float
    energy_consumed: float


# ==============================
# Feature Engineering Function
# ==============================

def generate_carbon_features(T_pred: datetime):

    T_now = carbon_history.index.max()
    recent = carbon_history.loc[:T_now]["Carbon intensity gCO₂eq/kWh (direct)"]

    # Time features from future timestamp
    hour = T_pred.hour
    day_of_week = T_pred.weekday()
    month = T_pred.month

    # Lag features from latest known data
    ci_lag_1 = recent.iloc[-1]
    ci_lag_2 = recent.iloc[-2]
    ci_lag_3 = recent.iloc[-3]
    ci_lag_6 = recent.iloc[-6]
    ci_lag_12 = recent.iloc[-12]
    ci_lag_24 = recent.iloc[-24]

    # Rolling features
    ci_roll_6 = recent.tail(6).mean()
    ci_roll_24 = recent.tail(24).mean()

    return np.array([[
        hour,
        day_of_week,
        month,
        ci_lag_1,
        ci_lag_2,
        ci_lag_3,
        ci_lag_6,
        ci_lag_12,
        ci_lag_24,
        ci_roll_6,
        ci_roll_24
    ]])

# ==============================
# Carbon Intensity Prediction
# ==============================

@app.post("/predict_carbon")
def predict_carbon(data: CarbonRequest):

    X = generate_carbon_features(data.timestamp)
    prediction = carbon_model.predict(X)

    return {
        "timestamp": data.timestamp,
        "predicted_carbon_intensity": round(float(prediction[0]), 3)
    }


# ==============================
# User Behaviour Clustering
# ==============================

@app.post("/cluster_user")
def cluster_user(data: UserClusterInput):

    X = np.array([[
        data.arrival_hour,
        data.charging_duration,
        data.energy_consumed
    ]])

    X_scaled = cluster_scaler.transform(X)
    cluster = cluster_model.predict(X_scaled)

    return {
        "user_cluster": int(cluster[0])
    }
