import sqlite3
conn = sqlite3.connect('audiophile.db')
c = conn.cursor()


def create_tables():
    c.execute('''CREATE TABLE if not exists fingerprint
             (quad UNSIGNED BIG INT PRIMARY KEY ON CONFLICT REPLACE,
              songid_time INTEGER)''')
    c.execute('''CREATE TABLE if not exists songs
              (songid UNSIGNED BIG INT PRIMARY KEY ON CONFLICT REPLACE,
               song_name TEXT,
               FOREIGN KEY(songid) REFERENCES fingerprint(songid_time))''')
    conn.commit()


def store(addresses, times, song_hash, song_name):
    create_tables()
    for i in range(len(addresses)):
        c.execute('INSERT into fingerprint VALUES (?, ?)',
                  (addresses[i], (song_hash << 13) + times[i]))
    c.execute('INSERT INTO songs VALUES (?, ?)', (song_hash, song_name))
    conn.commit()


def search(addresses, times):
    results = {}
    for i in range(len(addresses)):
        add = addresses[i]
        c.execute('SELECT songid_time FROM fingerprint WHERE quad = ?', (add,))
        info = c.fetchone()
        if info is not None:
            info = info[0]
            c.execute('SELECT song_name FROM songs WHERE songid = ?',
                      (info >> 13,))
            song_name = c.fetchone()[0]
            song_time = info & 8191
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
