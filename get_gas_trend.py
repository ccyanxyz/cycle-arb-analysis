from datetime import datetime
import json

ts = json.load(open('data/ts.json'))
stats = {}

with open('data/cycle_include_router.json') as f:
    for line in f:
        info = json.loads(line)
        t = ts[str(int(info['receipt']['blockNumber'], 16))]
        d = datetime.utcfromtimestamp(t).strftime('%Y-%m-%d')
        if d not in stats.keys():
            stats[d] = { 'gas_used': 0, 'gas_price': 0, 'cost': 0, 'count': 0 }
        if info['path'][0] != "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2":
            continue
        stats[d]['gas_used'] += int(info['receipt']['gasUsed'], 16)
        stats[d]['gas_price'] += int(info['tx']['gasPrice'], 16)
        stats[d]['cost'] += info['cost']
        stats[d]['count'] += 1

for k in stats.keys():
    item = stats[k]
    item['mean_gas_used'] = item['gas_used'] / item['count']
    item['mean_gas_price'] = item['gas_price'] / item['count']
    item['mean_gas_cost'] = item['cost'] / item['count']

json.dump(stats, open('data/gas_trend.json', 'w'))
