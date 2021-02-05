import json
from common import *

with open('data/cycle_include_router.json') as f:
    idx = 0
    for line in f:
        print(idx)
        info = json.loads(line)
        tx = w3.eth.getTransaction(info['receipt']['transactionHash'])
        with open('data/cycle_include_router_with_tx_from.json', 'a') as f1:
            f1.write(json.dumps({'tx': w3.toJSON(tx), 'receipt': info['receipt']}))
        idx += 1
