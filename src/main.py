import sound_util as su
import sys

try:
    if sys.argv[1] == 'learn':
        su.learn_song(sys.argv[2])
    elif sys.argv[1] == 'search':
        print(su.identify_clip(sys.argv[2]))
    elif sys.argv[1] == 'listen':
        print("not implemented yet!")
    else:
        raise Exception("Invalid option")
except Exception:
    print("Usage: \n")
    print("$ python main.py learn <path to audio file>")
    print("$ python main.py listen <time in seconds>")
    print("$ python main.py search <path to clip>")
