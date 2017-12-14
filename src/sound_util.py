import fingerprint as fp
import db

import soundfile as sf
import taglib
import hashlib
import os


def read_audiofile(filename):
    # get tags
    song = taglib.File(filename)
    assert song.length < 800, "Maximum allowed song length is 13 minutes"

    # get the signal
    name, ext = os.path.splitext(filename)
    os.system('ffmpeg -i %s %s%s' % (filename, name, '.wav'))
    _filename = name + '.wav'
    sig, fs = sf.read(_filename)  # extract the signal
    os.remove(_filename)

    return os.path.basename(filename), song.tags, sig


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


def identify_clip(filename):
    song_name, tags, sig = read_audiofile(filename)
    addresses, times = fp.get_addresses(fp.get_filtered_spectrogram(sig))

    return db.search(addresses)
