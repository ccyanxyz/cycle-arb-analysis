import json
from bisect import bisect
import linecache

bnidx = json.load(open('data/block_line_index.json'))
bns = [int(i) for i in bnidx.keys()]
def get_line(i):
    return linecache.getline('data/cycle_include_router_with_tx_from1.json', i).strip()

def search_frontrun(start, end, txinfo):
    frontrun_tx = None
    s = bisect(bns, start) - 1
    e = bisect(bns, end) + 1
    if s >= len(bns):
        sb = bns[-1]
    else:
        sb = bns[s]
    if e >= len(bns):
        eb = bns[-1]
    else:
        eb = bns[e]
    start_line = bnidx[str(sb)]
    end_line = bnidx[str(eb)]
    data = txinfo['input']
    for i in range(start_line, end_line):
        line = get_line(i)
        info = json.loads(line)
        bn = int(info['receipt']['blockNumber'], 16)
        if info['tx']['hash'] == txinfo['hash']:
            break
        if bn > end:
            break
        if info['tx']['input'] == data:
            frontrun_tx = info
            break
    return frontrun_tx

'''
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
'''

stats = {'frontrun': 0}
idx = 0
with open('data/failed_router_arbs.json') as f:
    for line in f:
        print(idx)
        idx += 1
        info = json.loads(line)
        bn = int(info['blockNumber'])
        f_tx = search_frontrun(bn - 20, bn, info)
        if not f_tx:
            continue
        with open('data/frontruned_arb_info.json', 'a') as f1:
            i = {'frontrun': f_tx, 'victim': info}
            f1.write(json.dumps(i)+'\n')
        stats['frontrun'] += 1
print(stats)
