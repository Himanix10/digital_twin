import numpy as np

def fuse_sensors(df, sensors):

    if len(sensors) == 0:
        raise ValueError("No sensors provided for fusion")

    sensor_data = df[sensors]

    fused_signal = sensor_data.mean(axis=1)

    return fused_signal.values