import numpy as np
from sklearn.linear_model import LinearRegression

def run_linear_regression(signal):

    signal = np.array(signal)

    X = np.arange(len(signal)).reshape(-1,1)

    model = LinearRegression()

    model.fit(X, signal)

    predicted = model.predict(X)

    return predicted