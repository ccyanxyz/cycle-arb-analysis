import json
from common import *

addrs = json.load(open('data/addrs.json'))
for i in range(10000835, 11709847):
    print(i)
    txcount = w3.eth.getBlockTransactionCount(i)
    for j in range(txcount):
        tx = w3.eth.getTransactionByBlock(i, j)
        if tx['to'] and tx['to'].lower() in addrs:
            rec = w3.eth.getTransactionReceipt(tx['hash'])
            if rec.status == 1:
                continue
            with open('/data/bot_txs', 'a') as f:
                info = {'tx': w3.toJSON(tx), 'receipt': w3.toJSON(rec)}
                f.write(json.dumps(info)+'\n')
