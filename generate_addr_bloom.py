import json
from eth_bloom import BloomFilter

data = json.load(open('data/addr_stats.json'))
b = BloomFilter()
for addr in data.keys():
    b.add(bytes(addr.encode()))
print(int(b))
print(bin(b))
