import json
from common import *

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

data = json.load(open('data/start_token_counts.json'))
addr2symbol = json.load(open('data/addr2symbol.json'))

top10 = list(data.keys())[:20]
bins = []
for k in top10:
    symbol = addr2symbol[k]
    bins.append(symbol)
print(bins)
bins.append('Other')
others = 0
for i in range(20, len(list(data.keys()))):
    k = list(data.keys())[i]
    others += data[k]

y = [data[k] for k in top10]
y.append(others)

plt.figure(figsize=(10, 6))
plt.bar(bins, y, color='r')
plt.xticks(bins, rotation=45)
# plt.xlabel('Ring Arbitrage Start Token')
plt.ylabel('Number of Arbitrage Txs')

plt.yscale('log', nonposy='clip')

for a, b in zip(bins, y):
    plt.text(a, b+0.05, b, ha='center', va='bottom', fontsize=7)

# plt.show()
plt.savefig('reports/start_token_counts.png')
