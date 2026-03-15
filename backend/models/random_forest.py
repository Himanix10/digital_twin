import numpy as np
from sklearn.ensemble import RandomForestRegressor

def run_random_forest(signal):

    signal = np.array(signal)

    X = np.arange(len(signal)).reshape(-1,1)

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, signal)

    predicted = model.predict(X)

    return predicted