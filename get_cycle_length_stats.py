import json

stats = {}
with open('data/cycle_include_router.json') as f:
    for line in f:
        info = json.loads(line)
        l = len(info['path'])/2
        if l not in stats.keys():
            stats[l] = 0
        stats[l] += 1
json.dump(stats, open('./data/cycle_length_stats.json', 'w'))
