import numpy as np

def fuse_sensors(filled_df, sensors):
    """
    Performs mean-based multi-sensor fusion.

    Parameters:
    - filled_df : DataFrame with cleaned sensor data
    - sensors   : list of selected sensor columns

    Returns:
    - fused_signal : numpy array representing system state
    """

    if len(sensors) == 1:
        fused_signal = filled_df[sensors[0]].values
    else:
        fused_signal = filled_df[sensors].mean(axis=1).values

    return fused_signal
