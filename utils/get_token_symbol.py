import json
from common import *

data = json.load(open('data/start_token_counts.json'))

d = {}
for addr in data.keys():
    try:
        s = get_symbol(addr)
        d[addr] = s
        print(addr, ':', s)
    except Exception as e:
        print(addr, e)

json.dump(d, open('data/addr2symbol.json', 'w'))
