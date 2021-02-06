import json

def sort_dict(d):
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[1]['profit'], reverse=True)}

router_count = 0
from_stats = {}
with open('data/cycle_include_router_with_tx_from1.json') as f:
    for line in f:
        info = json.loads(line)
        if info['tx']['to'] and info['tx']['to'].lower() == "0x7a250d5630b4cf539739df2c5dacb4c659f2488d":
            router_count += 1
            continue
        if info['path'][0] != '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2':
            continue
        _from = info['tx']['from']
        if _from not in from_stats.keys():
            from_stats[_from] = {'count': 0, 'profit': 0, 'revenue': 0, 'cost': 0}
        from_stats[_from]['count'] += 1
        from_stats[_from]['revenue'] += info['revenue']
        from_stats[_from]['cost'] += info['cost']
        from_stats[_from]['profit'] += info['revenue'] - info['cost']

from_stats = sort_dict(from_stats)
print(router_count)
json.dump(from_stats, open('data/eoa_stats_no_router.json', 'w'))
