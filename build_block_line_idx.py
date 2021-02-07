import json

stats = {}
idx = 0
with open('data/cycle_include_router_with_tx_from1.json') as f:
    for line in f:
        info = json.loads(line)
        bn = int(info['receipt']['blockNumber'], 16)
        if bn in stats.keys():
            idx += 1
            continue
        stats[bn] = idx
        idx += 1
json.dump(stats, open('data/block_line_index.json', 'w'))
