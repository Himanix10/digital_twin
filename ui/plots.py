import matplotlib.pyplot as plt
import numpy as np

def plot_system(actual, predicted, anomalies, future):

    fig, ax = plt.subplots(figsize=(12,5))

    ax.plot(actual, label="Actual")
    ax.plot(predicted, "--", label="Predicted")

    if future is not None and len(future) > 0:
        ax.plot(
            range(len(actual), len(actual)+len(future)),
            future,
            ":",
            label="Future"
        )

    if len(anomalies) > 0:
        ax.scatter(
            anomalies,
            np.array(actual)[anomalies],
            color="red",
            label="Anomaly",
            zorder=5
        )

    ax.legend()
    ax.grid(alpha=0.3)

    return fig
