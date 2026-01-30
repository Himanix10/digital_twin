import numpy as np
import pandas as pd

def compute_data_quality(numeric_df, sensors):
    """
    Computes data quality metrics:
    - Missing percentage
    - Noise level (std)
    - Outlier percentage
    - Quality score
    """

    total_cells = numeric_df[sensors].size

    # Missing values
    missing_pct = (
        numeric_df[sensors].isnull().sum().sum() / total_cells * 100
        if total_cells > 0 else 0
    )

    # Fill missing values (mean imputation)
    filled_df = numeric_df[sensors].fillna(numeric_df[sensors].mean())

    # Noise level
    noise = filled_df.std().mean()

    # Outlier detection (Z-score)
    z_scores = np.abs((filled_df - filled_df.mean()) / filled_df.std())
    outlier_pct = (z_scores > 3).sum().sum() / total_cells * 100

    # Overall data quality score
    quality_score = max(0, 100 - missing_pct - outlier_pct)

    return {
        "filled_df": filled_df,
        "missing_pct": missing_pct,
        "noise": noise,
        "outlier_pct": outlier_pct,
        "quality_score": quality_score
    }
