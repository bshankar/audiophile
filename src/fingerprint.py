import numpy as np
from scipy.signal import butter, lfilter, hamming


def lowpass_filter(sig, cutoff=5000, fs=44100, order=6):
    b, a = butter(order, cutoff / (0.5 * fs), analog=False)
    return lfilter(b, a, sig)


def truncate(sig, factor):
    return sig[: factor * (len(sig) // factor)]


def downsample(sig, factor=4):
    return np.mean(truncate(sig, factor).reshape(-1, factor), 1)


def apply_hamming(sig, fs=11025):
    window_size = fs // 10
    window = hamming(window_size, sym=False)
    sig = truncate(sig, window_size)
    return sig * np.tile(window, len(sig) // window_size)
