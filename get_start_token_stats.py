import json

def sort_dict(d):
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}

stats = {}

with open('data/cycle.json', 'r') as f:
    for line in f:
        info = json.loads(line)
        start = info['path'][0]
        if start not in stats.keys():
            stats[start] = 0
        stats[start] += 1
stats = sort_dict(stats)
json.dump(stats, open('data/start_token_counts.json', 'w'))
