import json
from web3.auto import w3

def is_uni_cycle(info):
    path = info['path']
    if len(path) < 6 or len(path) % 2 != 0:
        return None
    if path[0] != path[-1]:
        return None
    p = path[1:-1]
    for i in range(0, len(p), 2):
        if p[i] != p[i+1]:
            return None
    return info

with open('/data/new_uni_arb_info') as f:
    for line in f:
        info = json.loads(line)
        print(int(info['receipt']['blockNumber'], 16))
        if not is_uni_cycle(info):
            continue
        if info['tx']['to'] and w3.toChecksumAddress(info['tx']['to']) == '0x11111254369792b2Ca5d084aB5eEA397cA8fa48B':
            continue
        with open('data/cycle_include_router.json', 'a') as f2:
            f2.write(json.dumps(info)+'\n')
