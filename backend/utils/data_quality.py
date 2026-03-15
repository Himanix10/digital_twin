import numpy as np
import pandas as pd

def compute_data_quality(numeric_df, sensors):

    numeric_df = numeric_df.copy()

    numeric_df.columns = numeric_df.columns.str.strip().str.lower()

    sensors = [s.strip().lower() for s in sensors]

    sensors = [s for s in sensors if s in numeric_df.columns]

    if len(sensors) < 2:
        raise ValueError(f"Need at least 2 sensor columns. Available: {numeric_df.columns.tolist()}")

    sensor_df = numeric_df[sensors]

    total_cells = sensor_df.size

    missing_pct = (
        sensor_df.isnull().sum().sum() / total_cells * 100
        if total_cells > 0 else 0
    )

    filled_df = sensor_df.fillna(sensor_df.mean())

    noise = filled_df.std().mean()

    std = filled_df.std().replace(0, 1)

    z_scores = np.abs((filled_df - filled_df.mean()) / std)

    outlier_pct = (z_scores > 3).sum().sum() / total_cells * 100

    quality_score = max(0, 100 - missing_pct - outlier_pct)

    return {
        "filled_df": filled_df,
        "missing_pct": missing_pct,
        "noise": noise,
        "outlier_pct": outlier_pct,
        "quality_score": quality_score
    }