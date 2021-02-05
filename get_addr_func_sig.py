import json

stats = json.load(open('data/addr_stats.json'))

with open('data/cycle_include_router.json') as f:
    for line in f:
        info = json.loads(line)
        sig = info['tx']['input'][:10]
        addr = info['tx']['to']
        if not addr:
            continue
        if info['path'][0] != '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2':
            continue
        if 'sigs' not in stats[addr].keys():
            stats[addr]['sigs'] = []
        if sig not in stats[addr]['sigs']:
            stats[addr]['sigs'].append(sig)
json.dump(stats, open('data/addr_stats_with_sigs.json', 'w'))
