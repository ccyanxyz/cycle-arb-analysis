import json
from common import *

data = json.load(open('data/addr_stats.json'))
addrs = list(data.keys())

stats = {}
for addr in addrs:
    count = w3.eth.getTransactionCount(w3.toChecksumAddress(addr))
    print(addr, count)
    stats[addr] = count
json.dump(stats, open('data/addr_tx_count.json', 'w'))
