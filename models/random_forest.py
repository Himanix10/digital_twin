import numpy as np
from sklearn.ensemble import RandomForestRegressor

def run_random_forest(fused_signal):
    """
    Trains and predicts using Random Forest Regression.

    Parameters:
    - fused_signal : numpy array of fused system signal

    Returns:
    - predicted : model predictions
    """

    X = np.arange(len(fused_signal)).reshape(-1, 1)
    y = fused_signal

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)
    predicted = model.predict(X)

    return predicted
