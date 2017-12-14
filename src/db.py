import redis
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
            if song_name in results:
                results[song_name] += 1
            else:
                results[song_name] = 1
    return results
