from datetime import datetime
import json

ts = json.load(open('./data/ts.json'))
stats = {}
with open('./data/cycle_include_router.json') as f:
    for line in f:
        info = json.loads(line)
        t = ts[str(int(info['receipt']['blockNumber'], 16))]
        d = datetime.utcfromtimestamp(t).strftime('%Y-%m-%d') 
        if d not in stats.keys():
            stats[d] = { 'revenue': 0, 'cost': 0, 'count': 0 }
        if info['path'][0] != "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2":
            continue
        stats[d]['revenue'] += info['revenue']
        stats[d]['cost'] += info['cost']
        stats[d]['count'] += 1

json.dump(stats, open('data/daily_stats.json', 'w'))
