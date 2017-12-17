import fingerprint as fp
import db

import soundfile as sf
import taglib
import hashlib
import os
import glob
import sys


def convert_to_mono(sig):
    if len(sig.shape) > 1:
        return fp.np.mean(sig, axis=1)
    return sig


def read_audiofile(filename):
    # get tags
    song = taglib.File(filename)
    print(filename)
    assert song.length < 800, "Maximum allowed song length is 13 minutes"

    # get the signal
    name, ext = os.path.splitext(filename)
    os.system('ffmpeg -loglevel 8 -i "%s" "%s%s"' % (filename, name, '.wav'))
    _filename = name + '.wav'
    sig, fs = sf.read(_filename)  # extract the signal
    os.remove(_filename)

    return os.path.basename(filename), song.tags, convert_to_mono(sig)


def hash_metadata(filename, tags, bits=51):
    basename = os.path.basename(filename).encode('utf-8')
    m = hashlib.md5(b'%s' % basename)
    return int('0x' + m.hexdigest(), 16) >> (128 - bits)


def learn_song(filename):
    song_name, tags, sig = read_audiofile(filename)
    addresses, times = fp.get_addresses(fp.get_filtered_spectrogram(sig))

    basename = os.path.basename(filename)
    name, ext = os.path.splitext(basename)
    db.store(addresses, times, hash_metadata(filename, tags), name)


def learn_songs(_dir):
    for filename in glob.glob(_dir + '/**/*.[Mm]p3', recursive=True):
        song = taglib.File(filename)
        if song.length < 800:
            learn_song(filename)
        else:
            print('Skipping %s (too long)')


def identify_clip(filename):
    song_name, tags, sig = read_audiofile(filename)
    addresses, times = fp.get_addresses(fp.get_filtered_spectrogram(sig))
    return db.show_results(db.search(addresses, times), 3)


def identify_from_mic(time=20, sound_device=0):
    print("Listening...")
    filename = os.path.join(sys.path[0] + '/record.mp3')
    os.system('ffmpeg -loglevel 8 -ar 44100 -f alsa -i hw:%d -t %d %s' %
              (sound_device, time, filename))
    results = identify_clip(filename)
    os.remove(filename)
    return results
