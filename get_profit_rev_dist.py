import json

stats = { 'profits': [], 'revenues': [], 'costs': [] }

with open('data/cycle_include_router.json') as f:
    for line in f:
        info = json.loads(line)
        if info['path'][0] != "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2":
            continue
        stats['revenues'].append(info['revenue'])
        stats['profits'].append(info['revenue']-info['cost'])
        stats['costs'].append(info['cost'])
json.dump(stats, open('data/profit_revenue_cost.json', 'w'))
