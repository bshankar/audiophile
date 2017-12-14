import redis
import numpy as np
r = redis.StrictRedis()


def store(addresses, times, song_hash, song_name):
    for i in range(len(addresses)):
        r.set('note:' + str(addresses[i]), (song_hash << 13) + times[i])
    r.set('song:%d' % song_hash, song_name)


def search(addresses):
    results = {}
    for add in addresses:
        info = r.get('note:' + str(add))
        if info is not None:
            song_name = r.get('song:' + str(int(info) >> 13))
            song_time = int(info) & 8191
            if song_name in results:
                results[song_name][0] += 1
                dt = song_time - results[song_name][2]
                if dt == 1:
                    results[song_name][1] += 1
                results[song_name][2] = song_time
            else:
                results[song_name] = [1, 0, song_time]
    return {s: [results[s][0], results[s][1]] for s in results}
