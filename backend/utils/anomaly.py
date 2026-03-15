import numpy as np

def compute_anomalies_and_health(actual, predicted):

    actual = np.array(actual)
    predicted = np.array(predicted)

    error = np.abs(actual - predicted)

    threshold = error.mean() + 2 * error.std()

    anomalies = np.where(error > threshold)[0]

    health = 100 - (error / (np.max(error) + 1e-6) * 100)

    return anomalies, error, health