import matplotlib.pyplot as plt
from fingerprint import np, lowpass_filter, downsample


def lowpass_filter_test():
    fs = 30
    t = np.linspace(0, 5, 5 * fs, endpoint=False)
    sig = np.sin(1.2 * 2 * np.pi * t) + \
        1.5 * np.cos(9 * 2 * np.pi * t) + \
        0.5 * np.sin(12.0 * 2 * np.pi * t)

    plt.plot(t, sig, color='red')
    sig_filtered = lowpass_filter(sig, 3.667, 30, 6)
    plt.plot(t, sig_filtered, color='blue')
    plt.show()


def downsample_test():
    a = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    print(downsample(a, 3))


if __name__ == "__main__":
    downsample_test()
