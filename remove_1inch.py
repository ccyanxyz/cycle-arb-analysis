import json
from web3.auto import w3

with open('/data/new_uni_arb_info') as f:
    for line in f:
        info = json.loads(line)
        print(int(info['receipt']['blockNumber'], 16))
        if info['tx']['to'] and w3.toChecksumAddress(info['tx']['to']) == '0x11111254369792b2Ca5d084aB5eEA397cA8fa48B':
            continue
        with open('data/cycle_include_router.json', 'a') as f2:
            f2.write(json.dumps(info)+'\n')
