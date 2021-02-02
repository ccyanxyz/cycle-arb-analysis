import json
from common import *

addrs = json.load(open('data/addrs.json'))
for i in range(10000835, 11709847):
    txcount = w3.eth.getBlockTransactionCount(i)
    print(i)
    for j in range(txcount):
        tx = w3.eth.getTransactionByBlock(i, j)
        if tx['to'] in addrs:
            rec = w3.eth.getTransactionReceipt(tx['hash'])
            if rec.status == 1:
                continue
            with open('/data/bot_txs', 'a') as f:
                f.write(json.dumps({'tx': tx, 'receipt': rec})+'\n')
