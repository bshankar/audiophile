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


def get_spectrograms(sig):
    return apply_fft(apply_hamming(downsample(lowpass_filter(sig))))


def get_strongest_bins(spg):
    band_ranges = [[0, 10],  [10, 20], [20, 40],
                   [40, 80], [80, 160], [160, 511]]
    return np.array([(np.argmax(spg[start: end]), np.max(spg[start: end]))
                     for start, end in band_ranges])


get_strongest_bins = np.vectorize(get_strongest_bins, signature='(m)->(n,p)')


def global_strongest_amplitudes_mean(bins):
    print(np.max(bins[..., 1], axis=0))
    return np.mean(np.max(bins[..., 1], axis=0))


def get_filtered_spectrogram(sig, k=0.05):
    spgs = get_spectrograms(sig)
    bins = get_strongest_bins(spgs)
    mean = global_strongest_amplitudes_mean(bins)
    return [[int(bins[i, j, 0]) for j in range(6) if bins[i, j, 1] > k * mean]
            for i in range(len(bins))]
