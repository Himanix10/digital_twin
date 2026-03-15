import numpy as np

def run_lstm(signal, scaler):

    signal = np.array(signal)

    # simulate sequential prediction
    predicted = np.roll(signal, -1)

    # add small noise to simulate prediction variance
    predicted = predicted + np.random.normal(0, 0.05, len(signal))

    return signal, predicted