import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input

def run_autoencoder(fused_signal, scaler):
    """
    Trains an Autoencoder and returns reconstructed signal.

    Parameters:
    - fused_signal : numpy array (original scale)
    - scaler       : MinMaxScaler

    Returns:
    - actual       : scaled actual signal
    - reconstructed: reconstructed signal from autoencoder
    """

    # Scale data
    data_scaled = scaler.fit_transform(fused_signal.reshape(-1, 1))

    # Autoencoder architecture
    input_layer = Input(shape=(1,))
    encoded = Dense(16, activation="relu")(input_layer)
    encoded = Dense(8, activation="relu")(encoded)
    decoded = Dense(16, activation="relu")(encoded)
    output_layer = Dense(1)(decoded)

    autoencoder = Model(input_layer, output_layer)
    autoencoder.compile(optimizer="adam", loss="mse")

    autoencoder.fit(
        data_scaled,
        data_scaled,
        epochs=30,
        batch_size=16,
        verbose=0
    )

    reconstructed = autoencoder.predict(data_scaled, verbose=0).flatten()
    actual = data_scaled.flatten()

    return actual, reconstructed
