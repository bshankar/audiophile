import numpy as np
from scipy.signal import butter, lfilter


def lowpass_filter(sig, cutoff=5000, fs=44100, order=6):
    b, a = butter(order, cutoff / (0.5 * fs), analog=False)
    return lfilter(b, a, sig)


def downsample(arr, factor=4):
    end = factor * (len(arr) // factor)
    return np.mean(arr[:end].reshape(-1, factor), 1)
