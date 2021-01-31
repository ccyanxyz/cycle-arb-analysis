import json
from datetime import datetime
import numpy as np

def sort_dict(d):
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[1]['revenue'], reverse=True)}

ts = json.load(open('data/ts.json'))
botstats = json.load(open('data/bot_stats.json'))
sorted_botstats = sort_dict(botstats)

top10 = list(sorted_botstats.keys())[:10]
print(top10, len(top10))

stats = {}
for addr in top10:
    stats[addr] = {}

with open('./data/cycle_include_router.json') as f:
    for line in f:
        info = json.loads(line)
        t = ts[str(int(info['receipt']['blockNumber'], 16))]
        d = datetime.utcfromtimestamp(t).strftime('%Y-%m-%d')
        if info['tx']['to'] not in top10:
            continue
        if info['path'][0] != '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2':
            continue
        addr = info['tx']['to']
        if d not in stats[addr].keys():
            stats[addr][d] = { 'revenue': 0, 'cost': 0, 'count': 0, 'profit': 0 }
        stats[addr][d]['revenue'] += info['revenue']
        stats[addr][d]['cost'] += info['cost']
        stats[addr][d]['profit'] += info['revenue']-info['cost']
        stats[addr][d]['count'] += 1

json.dump(stats, open('data/top10_rev_bot_daily_stats.json', 'w'))
