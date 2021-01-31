import json
from common import *

data = json.load(open('data/path_counts.json'))

top10 = list(data.keys())[:10]
d = {}
for p in top10:
    arr = p.strip().split('-')
    s = []
    for item in arr:
        if item == '-' or item == '\n' or item == '':
            continue
        try:
            symbol = get_symbol(item)
        except:
            # raise
            symbol = item
        s.append(symbol)
    s = list(set(s))
    print(s)
    d[p] = s
json.dump(d, open('data/top10_path_symbols.json', 'w'))
