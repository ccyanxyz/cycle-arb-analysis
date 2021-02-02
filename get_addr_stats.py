import json

def sort_dict(d):
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[1]['profit'], reverse=True)}

to_stats = {}
from_stats = {}
with open('data/cycle_include_router.json') as f:
    for line in f:
        info = json.loads(line)
        if info['path'][0] != '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2':
            continue
        # _from = info['tx']['from']
        # if _from not in from_stats.keys():
            # from_stats[_from] = {'count': 0, 'profit': 0, 'revenue': 0, 'cost': 0}
        # from_stats[_from]['count'] += 1
        # from_stats[_from]['revenue'] += info['revenue']
        # from_stats[_from]['cost'] += info['cost']
        # from_stats[_from]['profit'] += info['revenue'] - revenue['cost']

        if not info['tx']['to']:
            continue
        to = info['tx']['to']
        if to not in to_stats.keys():
            to_stats[to] = {'count': 0, 'profit': 0, 'revenue': 0, 'cost': 0}
        to_stats[to]['count'] += 1
        to_stats[to]['revenue'] += info['revenue']
        to_stats[to]['cost'] += info['cost']
        to_stats[to]['profit'] += info['revenue'] - info['cost']

# from_stats = sort_dict(from_stats)
to_stats = sort_dict(to_stats)
# stats =  {'from': from_stats, 'to': to_stats}
# json.dump(stats, open('data/addr_stats.json', 'w'))
json.dump(to_stats, open('data/addr_stats.json', 'w'))
