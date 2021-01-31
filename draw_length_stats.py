import json
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

def sort_dict(d):
    return {k: v for k, v in sorted(d.items(), key=lambda item: int(item[0]), reverse=False)}

data = json.load(open('data/cycle_length_stats.json'))
data = sort_dict(data)

bins = [k for k in data.keys()]
y = [data[k] for k in data.keys()]

plt.bar(bins, y, color='b')
# plt.xticks(bins)
plt.xlabel('Arbitrage Path Length')
plt.ylabel('Number of Arbitrage Txs')

plt.yscale('log', nonposy='clip')

for a, b in zip(bins, y):
    plt.text(a, b+0.05, b, ha='center', va='bottom', fontsize=7)

# plt.show()
plt.savefig('reports/cycle_length.png')
