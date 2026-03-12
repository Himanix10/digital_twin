import numpy as np
from sklearn.linear_model import LinearRegression

def run_linear_regression(fused_signal):
    """
    Trains and predicts using Linear Regression.

    Parameters:
    - fused_signal : numpy array of fused system signal

    Returns:
    - predicted : model predictions
    """

    X = np.arange(len(fused_signal)).reshape(-1, 1)
    y = fused_signal

    model = LinearRegression()
    model.fit(X, y)

    predicted = model.predict(X)

    return predicted
