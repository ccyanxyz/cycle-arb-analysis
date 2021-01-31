import numpy as np
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import json

stats = json.load(open('data/profit_revenue.json'))
profits = [t/1e18 for t in stats['profits']]
revenues = [t/1e18 for t in stats['revenues']]

print('len:', len(profits))
# count = 0
# for t in profits:
    # if t >= -0.1 and t <= 0.7:
        # count += 1
# print(count)

bins = []
start = -0.1
while start < 0.7:
    bins.append(start)
    start += 0.01
bins = np.array(bins)

plt.hist(profits, bins, color='b', alpha=0.5, label='profit')
plt.hist(revenues, bins, color='r', alpha=0.5, label='revenue')
plt.xlabel('Amount(ETH)')
plt.ylabel('Number of Arbitrage Txs')
plt.legend()
plt.savefig('reports/profit_rev_distribution.png')
plt.show()
