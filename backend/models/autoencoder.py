import numpy as np

def run_autoencoder(signal, scaler):

    signal = np.array(signal)

    # simulate reconstruction
    reconstructed = signal + np.random.normal(0, 0.05, len(signal))

    return signal, reconstructed