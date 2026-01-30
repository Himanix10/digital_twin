import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def _create_sequences(data, window_size=10):
    """
    Creates sliding window sequences for LSTM.
    """
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i + window_size])
        y.append(data[i + window_size])
    return np.array(X), np.array(y)

def run_lstm(fused_signal, scaler, window_size=10):
    """
    Trains and predicts using LSTM.

    Parameters:
    - fused_signal : numpy array (original scale)
    - scaler       : fitted MinMaxScaler
    - window_size  : time window size

    Returns:
    - actual       : actual values
    - predicted    : LSTM predictions
    """

    # Scale data
    data_scaled = scaler.fit_transform(fused_signal.reshape(-1, 1))

    # Create sequences
    X, y = _create_sequences(data_scaled, window_size)

    # Build LSTM model
    model = Sequential([
        LSTM(50, activation="relu", input_shape=(X.shape[1], 1)),
        Dense(1)
    ])

    model.compile(optimizer="adam", loss="mse")
    model.fit(X, y, epochs=10, batch_size=8, verbose=0)

    # Predict
    predictions = model.predict(X, verbose=0)

    # Inverse scale
    predicted = scaler.inverse_transform(predictions).flatten()
    actual = scaler.inverse_transform(y).flatten()

    return actual, predicted
