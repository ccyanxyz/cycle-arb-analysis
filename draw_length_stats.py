import json
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

def sort_dict(d):
    return {k: v for k, v in sorted(d.items(), key=lambda item: int(float(item[0])), reverse=False)}

data = json.load(open('data/len_stats_new.json'))
data = sort_dict(data)

bins = [int(float(k)) for k in data.keys()]
print(bins)
y = [data[k] for k in data.keys()]

plt.figure(figsize=(10, 6))
plt.bar(bins, y, color='b')
plt.xticks(bins)
plt.xlabel('Arbitrage Cycle Length')
plt.ylabel('Number of Arbitrage Cycles')

plt.yscale('log', nonposy='clip')

for a, b in zip(bins, y):
    plt.text(a, b+0.05, b, ha='center', va='bottom', fontsize=7)

# plt.show()
plt.savefig('reports/cycle_length.png')
