import sound_util as su
import sys

try:
    if sys.argv[1] == 'learn':
        su.learn_song(sys.argv[2])
    elif sys.argv[1] == 'learnall':
        su.learn_songs(sys.argv[2])
    elif sys.argv[1] == 'search':
        print(su.identify_clip(sys.argv[2]))
    elif sys.argv[1] == 'listen':
        print(su.identify_from_mic(int(sys.argv[2], int(sys.argv[3]))))
    else:
        raise Exception("Invalid option")
except Exception:
    print("Usage: \n")
    print("$ python main.py learn <path to audio file>")
    print("$ python main.py learn <directory containing audio files>")
    print("$ python main.py listen <time in seconds> <sound device index>")
    print("$ python main.py search <path to clip>")

    raise Exception
