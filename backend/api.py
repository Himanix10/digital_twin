from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from ai.explainer import generate_explanation
app = FastAPI(title="Hybrid Digital Twin API")

# -----------------------------
# CORS for React frontend
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Root
# -----------------------------
@app.get("/")
def home():
    return {"message": "Hybrid Digital Twin API running"}

# -----------------------------
# Run ML Model
# -----------------------------
@app.post("/run-model")
async def run_model(data: dict):

    try:

        from utils.data_quality import compute_data_quality
        from utils.fusion import fuse_sensors
        from utils.anomaly import compute_anomalies_and_health

        df = pd.DataFrame(data["data"])
        sensors = data["sensors"]
        model_type = data["model"]

        numeric_df = df.select_dtypes(include=np.number)

        dq = compute_data_quality(numeric_df, sensors)

        fused = fuse_sensors(dq["filled_df"], sensors)

        scaler = MinMaxScaler()

        # -----------------------------
        # Model Selection (Lazy Load)
        # -----------------------------

        if model_type == "Linear Regression":

            from models.linear_model import run_linear_regression
            actual = fused
            predicted = run_linear_regression(fused)

        elif model_type == "Random Forest":

            from models.random_forest import run_random_forest
            actual = fused
            predicted = run_random_forest(fused)

        elif model_type == "LSTM":

            from models.lstm_model import run_lstm
            actual, predicted = run_lstm(fused, scaler)

        else:

            from models.autoencoder import run_autoencoder
            actual, predicted = run_autoencoder(fused, scaler)

        anomalies, error, health = compute_anomalies_and_health(actual, predicted)

        return {
            "actual": actual.tolist(),
            "predicted": predicted.tolist(),
            "anomalies": anomalies.tolist(),
            "health": float(np.mean(health)),
            "noise": float(dq["noise"])
        }

    except Exception as e:

        return {"error": str(e)}

# -----------------------------
# AI Explanation
# -----------------------------
@app.post("/explain")
async def explain(data: dict):

    try:

        from ai.explainer import generate_explanation

        health = data["health"]
        anomalies = data["anomalies"]
        noise = data["noise"]

        prompt = f"health:{int(health)}\nanomalies:{anomalies}\nnoise:{int(noise)}"

        explanation = generate_explanation(prompt)

        return {"explanation": explanation}

    except Exception as e:

        return {"error": str(e)}