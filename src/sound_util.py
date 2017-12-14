import soundfile as sf
import os
import taglib


def read_mp3(filename):
    # get tags
    song = taglib.File(filename)

    # get the signal
    name, ext = os.path.splitext(filename)
    os.system('ffmpeg -i %s %s%s' % (filename, name, '.wav'))
    _filename = name + '.wav'
    sig, fs = sf.read(_filename)  # extract the signal
    os.remove(_filename)

    return os.path.basename(filename), song.tags, sig
