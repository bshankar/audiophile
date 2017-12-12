import numpy as np
from scipy.signal import butter, lfilter, hamming


def lowpass_filter(sig, cutoff=5000, fs=44100, order=6):
    b, a = butter(order, cutoff / (0.5 * fs), analog=False)
    return lfilter(b, a, sig)


def truncate(sig, fac):
    return sig[: fac * (len(sig) // fac)]


def downsample(sig, fac=4):
    return np.mean(truncate(sig, fac).reshape(-1, fac), 1)


def apply_hamming(sig, ws=1024):
    window = hamming(ws, sym=False)
    sig = truncate(sig, ws)
    return sig * np.tile(window, len(sig) // ws)


def apply_fft(sig, fs=11025, ws=1024):
    return np.abs(np.fft.rfft(sig.reshape(-1, ws)))


def strongest_bins(spg):
    band_ranges = [[0, 10],  [10, 20], [20, 40],
                   [40, 80], [80, 160], [160, 511]]

    return [np.argmax(spg[start: end + 1])
            for start, end in band_ranges]


def global_strongest_bins_mean(spg):
    pass
