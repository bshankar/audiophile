import soundfile as sf
import os


def readSound(filename):
    name, ext = os.path.splittext(filename)
    if ext != '.wav':
        os.system('ffmpeg -i %s -o %s%s' % (filename, name, ext))

    filename = name + ext
    return sf.read(filename)
