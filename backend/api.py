import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

app = FastAPI(title="Hybrid Digital Twin API")


# ─────────────────────────────────────
# CORS (REQUIRED FOR REACT)
# ─────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────
# REQUEST MODELS
# ─────────────────────────────────────

class RunModelRequest(BaseModel):
    data: List[Dict[str, Any]]
    sensors: List[str]
    model: str
    horizon: int


class ExplainRequest(BaseModel):
    health: float
    anomalies: int
    noise: float


# ─────────────────────────────────────
# ROOT
# ─────────────────────────────────────

@app.get("/")
def home():
    return {"message": "Hybrid Digital Twin API running"}


# ─────────────────────────────────────
# CSV PREVIEW
# ─────────────────────────────────────
@app.post("/preview-csv")
async def preview_csv(file: UploadFile = File(...)):

    try:

        print("CSV PREVIEW START")

        df = pd.read_csv(file.file)

        df.columns = df.columns.str.strip().str.lower()

        # remove index columns
        df = df.loc[:, ~df.columns.str.contains("^unnamed")]

        # replace invalid numeric values
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna(0)

        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        preview = df.head(5)

        print("CSV PREVIEW DONE")

        return {
            "columns": df.columns.tolist(),
            "numeric_columns": numeric_cols,
            "rows_preview": preview.to_dict(orient="records")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────
# CSV MODEL RUN
# ─────────────────────────────────────

@app.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    sensors: str = Form(""),
    model: str = Form("Random Forest")
):

    try:

        print("STEP 1 CSV: reading file")

        from utils.data_quality import compute_data_quality
        from utils.fusion import fuse_sensors
        from utils.anomaly import compute_anomalies_and_health

        df = pd.read_csv(file.file)

        df.columns = df.columns.str.strip().str.lower()

        df = df.loc[:, ~df.columns.str.contains("^unnamed")]

        numeric_df = df.select_dtypes(include=np.number)

        if len(numeric_df.columns) == 0:
            raise HTTPException(
                status_code=400,
                detail="CSV must contain numeric sensor columns."
            )

        if sensors:

            sensors = [s.strip().lower() for s in sensors.split(",")]

            sensors = [s for s in sensors if s in numeric_df.columns]

            if len(sensors) == 0:
                raise HTTPException(
                    status_code=400,
                    detail="Selected sensors not found in dataset."
                )

        else:
            sensors = numeric_df.columns.tolist()

        print("STEP 2 CSV: sensors selected", sensors)

        dq = compute_data_quality(numeric_df, sensors)

        print("STEP 3 CSV: data quality complete")

        fused = fuse_sensors(dq["filled_df"], sensors)

        print("STEP 4 CSV: fusion complete")

        scaler = MinMaxScaler()

        print("STEP 5 CSV: running model", model)

        if model == "Linear Regression":

            from models.linear_model import run_linear_regression
            actual = fused
            predicted = run_linear_regression(fused)

        elif model == "Random Forest":

            from models.random_forest import run_random_forest
            actual = fused
            predicted = run_random_forest(fused)

        elif model == "LSTM":

            from models.lstm_model import run_lstm
            actual, predicted = run_lstm(fused, scaler)

        else:

            from models.autoencoder import run_autoencoder
            actual, predicted = run_autoencoder(fused, scaler)

        print("STEP 6 CSV: model finished")

        anomalies, error, health = compute_anomalies_and_health(actual, predicted)

        print("STEP 7 CSV: anomaly detection done")

        # FIX JSON CRASH
        actual = np.nan_to_num(actual)
        predicted = np.nan_to_num(predicted)
        anomalies = np.nan_to_num(anomalies)

        health_val = float(np.nan_to_num(np.mean(health)))
        noise_val = float(np.nan_to_num(dq["noise"]))

        return {
            "actual": actual.tolist(),
            "predicted": predicted.tolist(),
            "anomalies": anomalies.tolist(),
            "health": health_val,
            "noise": noise_val,
            "sensors_used": sensors
        }

    except Exception as e:

        import traceback
        traceback.print_exc()

        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────
# SIMULATED DATA MODEL RUN
# ─────────────────────────────────────

@app.post("/run-model")
async def run_model(request: RunModelRequest):

    try:

        print("STEP 1: request received")

        from utils.data_quality import compute_data_quality
        from utils.fusion import fuse_sensors
        from utils.anomaly import compute_anomalies_and_health

        df = pd.DataFrame(request.data)

        if df.empty:
            raise HTTPException(status_code=400, detail="No data received")

        df.columns = df.columns.str.strip().str.lower()

        numeric_df = df.select_dtypes(include=np.number)

        if numeric_df.shape[1] == 0:
            raise HTTPException(
                status_code=400,
                detail="No numeric columns in data"
            )

        sensors = [s.lower() for s in request.sensors]

        sensors = [s for s in sensors if s in numeric_df.columns]

        if len(sensors) == 0:
            sensors = numeric_df.columns.tolist()

        print("STEP 2: sensors selected", sensors)

        dq = compute_data_quality(numeric_df, sensors)

        print("STEP 3: data quality complete")

        fused = fuse_sensors(dq["filled_df"], sensors)

        print("STEP 4: sensor fusion complete")

        scaler = MinMaxScaler()

        model_type = request.model

        print("STEP 5: running model", model_type)

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

        print("STEP 6: model completed")

        anomalies, error, health = compute_anomalies_and_health(actual, predicted)

        print("STEP 7: anomaly detection complete")

        # FIX JSON CRASH
        actual = np.nan_to_num(actual)
        predicted = np.nan_to_num(predicted)
        anomalies = np.nan_to_num(anomalies)

        health_val = float(np.nan_to_num(np.mean(health)))
        noise_val = float(np.nan_to_num(dq["noise"]))

        return {
            "actual": actual.tolist(),
            "predicted": predicted.tolist(),
            "anomalies": anomalies.tolist(),
            "health": health_val,
            "noise": noise_val,
            "sensors_used": sensors
        }

    except Exception as e:

        import traceback
        traceback.print_exc()

        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────
# AI EXPLANATION
# ─────────────────────────────────────

@app.post("/explain")
async def explain(request: ExplainRequest):

    try:

        from ai.explainer import generate_explanation

        prompt = f"health:{int(request.health)} anomalies:{request.anomalies} noise:{int(request.noise)}"

        explanation = generate_explanation(prompt)

        return {"explanation": explanation}

    except Exception as e:

        import traceback
        traceback.print_exc()

        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────
# MAIN
# ─────────────────────────────────────

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )