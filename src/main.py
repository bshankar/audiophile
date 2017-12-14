import sound_util as su
import sys

try:
    if sys.argv[1] == 'learn':
        su.learn_song(sys.argv[2])
    elif sys.argv[1] == 'search':
        su.identify_clip(sys.argv[2])
    elif sys.argv[1] == 'listen':
        print("not implemented yet!")
    else:
        raise Exception("Invalid option")
except Exception:
    print("Learn a song: $ python main.py learn <path to audio file>")
    print("Listen to mic: $ python main.py listen <time>")
    print("Search an audio clip: $ python main.py search <path to clip>")
