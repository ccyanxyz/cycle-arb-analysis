import json
from common import *

f = open('data/cycle_include_router.json')
f1 = open('data/cycle_include_router_with_tx_from.json')
idx = 0
for line in f:
    print(idx)
    info = json.loads(line)
    l1 = next(f1)
    info1 = json.loads(l1)
    info['tx'] = info1['tx']
    with open('data/cycle_include_router_with_tx_from1.json', 'a') as f2:
        f2.write(json.dumps(info)+'\n')
    idx += 1
