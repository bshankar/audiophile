import fingerprint as fp
import db

import soundfile as sf
import taglib
import hashlib
import os


def read_mp3(filename):
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


def hash(filename, tags, bits=51):
    basename = os.path.basename(filename).encode('utf-8')
    m = hashlib.md5(b'%s' % basename)
    return int('0x' + m.hexdigest(), 16) >> (128 - bits)
