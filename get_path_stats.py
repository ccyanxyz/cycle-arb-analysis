from datetime import datetime
import json

def get_key(addrs):
    s = sorted(addrs)
    ret = ""
    for t in s:
        ret += t
        ret += '-'
    return ret

ts = json.load(open('data/ts.json'))
stats = {}
count = {}
with open('data/cycle_include_router.json') as f:
    for line in f:
        info = json.loads(line)
        t = ts[str(int(info['receipt']['blockNumber'], 16))]
        d = datetime.utcfromtimestamp(t).strftime('%Y-%m-%d')

        p = get_key(info['path'])
        if p not in count.keys():
            count[p] = 0
        count[p] += 1
        if p not in stats.keys():
            stats[p] = {}
        if d not in stats[p].keys():
            stats[p][d] = 0
        stats[p][d] += 1

def sort_dict(d):
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}

count = sort_dict(count)
json.dump(count, open('data/path_counts.json', 'w'))

with open('data/daily_path_stats.json', 'w') as f:
    print('total paths:', len(stats.keys()))
    json.dump(stats, f)
