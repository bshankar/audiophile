import redis
import operator
r = redis.StrictRedis()


def store(addresses, times, song_hash, song_name):
    for i in range(len(addresses)):
        r.set('note:' + str(addresses[i]), (song_hash << 13) + times[i])
    r.set('song:%d' % song_hash, song_name)


def search(addresses, times):
    results = {}
    for i in range(len(addresses)):
        add = addresses[i]
        info = r.get('note:' + str(add))
        if info is not None:
            song_name = r.get('song:' + str(int(info) >> 13))
            song_time = int(info) & 8191
            if song_name in results:
                results[song_name][0] += 1
                results[song_name][1].append(song_time - times[i])
            else:
                results[song_name] = [1, [song_time - times[i]]]

    return filter_results(results)


def filter_results(results):
    filtered = {}
    for s in results:
        dts = {i: results[s][1].count(i) for i in results[s][1]}
        dts_matched = max(dts.values())
        if dts_matched > 10:
            filtered[s] = (results[s][0], dts_matched)
    return filtered


def show_results(filtered_results, best=10):
    top_results = sorted(filtered_results.keys(),
                         key=lambda i: filtered_results[i][1], reverse=True)

    to_print = ''
    for i in top_results[:best]:
        to_print += "%s    %d quads    %d coherent quads\n" \
            % (i, filtered_results[i][0], filtered_results[i][1])
    return to_print
