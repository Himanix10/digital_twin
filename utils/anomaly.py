import numpy as np

def compute_anomalies_and_health(actual, predicted):
    """
    Computes anomaly indices and system health score.

    Parameters:
    - actual    : numpy array of actual system signal
    - predicted : numpy array of model output

    Returns:
    - anomalies : indices where anomaly is detected
    - error     : absolute prediction error
    - health    : system health score (0–100)
    """

    error = np.abs(actual - predicted)

    # Anomaly detection using statistical threshold
    threshold = error.mean() + 3 * error.std()
    anomalies = np.where(error > threshold)[0]

    # Health score calculation
    health = max(0, 100 - (error.mean() / (error.max() + 1e-6)) * 100)

    return anomalies, error, health
