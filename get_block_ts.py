from common import *
import json

start = 10000835
end = 11731968

d = {}
for i in range(start, end+1):
    print(i, '/', end)
    blk = w3.eth.getBlock(i)
    d[i] = blk['timestamp']
json.dump(d, open('data/ts.json', 'w'))
