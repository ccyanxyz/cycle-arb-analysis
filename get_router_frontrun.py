import json

def search_frontrun(start, end, data):
    frontrun_tx = None
    with open('data/cycle_include_router_with_tx_from1.json') as f:
        for line in f:
            info = json.loads(line)
            bn = int(info['receipt']['blockNumber'], 16)
            if bn < start:
                continue
            if bn > end:
                break
            if info['tx']['input'] == data:
                frontrun_tx = info
    return frontrun_tx

stats = {'frontrun': 0}
with open('data/failed_router_arbs.json') as f:
    for line in f:
        info = json.loads(line)
        bn = int(info['blockNumber'])
        f_tx = search_frontrun(bn - 20, bn, info['input'])
        if not f_tx:
            continue
        with open('data/frontruned_arb_info.json', 'a') as f1:
            i = {'frontrun': f_tx, 'victim': info}
        stats['frontrun'] += 1
print(stats)
