import json
from common import *

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

data = json.load(open('data/start_token_counts.json'))

bins = []
for k in data.keys():
    symbol = get_symbol(k)
    bins.append(symbol)
print(bins)

y = [data[k] for k in data.keys()]

plt.bar(bins, y, color='r')
plt.xticks(bins, rotation=45)
plt.xlabel('Ring Arbitrage Start Token')
plt.ylabel('Number of Arbitrage Txs')

plt.yscale('log', nonposy='clip')

for a, b in zip(bins, y):
    plt.text(a, b+0.05, b, ha='center', va='bottom', fontsize=7)

plt.show()
plt.savefig('reports/start_token_counts.png')
