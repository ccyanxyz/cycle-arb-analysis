import json

stats = {}
with open('data/cycle_include_router.json') as f:
    for line in f:
        info = json.loads(line)
        path = info['path']
        amounts = info['amounts']
        start = path[0]
        if start != '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2':
            continue
        last_start = 0
        i = 1
        while i < len(path):
            if path[i] == start:
                l = (i + 1 - last_start)/2
                if l not in stats.keys():
                    stats[l] = {'count': 0, 'revenue': 0, 'avg_revenue': 0}
                stats[l]['count'] += 1
                stats[l]['revenue'] += amounts[i] - amounts[last_start]
                stats[l]['avg_revenue'] = stats[l]['revenue'] / stats[l]['count']
                if i < len(path) - 1:
                    last_start = i+1
                    i += 1
            i += 1
print(stats)
json.dump(stats, open('data/avg_revenue_cycle_length.json', 'w'))
