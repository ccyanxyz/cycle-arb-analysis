import json

stats = {}
with open('data/cycle_include_router.json', 'r') as f:
    for line in f:
        info = json.loads(line)
        if not info['tx']['to']:
            continue
        to = info['tx']['to']
        if info['path'][0] != '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2':
            continue
        if to not in stats.keys():
            stats[to] = { 'revenue': 0, 'cost': 0, 'profit': 0, 'count': 0}
        stats[to]['count'] += 1
        stats[to]['revenue'] += info['revenue']
        stats[to]['cost'] += info['cost']
        stats[to]['profit'] += info['cost']
json.dump(stats, open('data/bot_stats.json', 'w'))
