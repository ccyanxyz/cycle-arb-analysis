import numpy as np
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import json

stats = json.load(open('data/profit_revenue_cost.json'))
profits = [t/1e18 for t in stats['profits']]
revenues = [t/1e18 for t in stats['revenues']]
costs = [t/1e18 for t in stats['costs']]

print('len:', len(profits))
# count = 0
# for t in profits:
    # if t >= -0.1 and t <= 0.7:
        # count += 1
# print(count)

bins = []
start = -0.1
while start < 0.4:
    bins.append(start)
    start += 0.01
bins = np.array(bins)

# profit distribution
plt.hist(profits, bins, color='b', alpha=0.5, label='profit')
plt.xlabel('Amount(ETH)')
plt.ylabel('Number of Arbitrage Txs')
plt.legend()
plt.savefig('reports/profit_dist.png')
plt.clf()

# revenue distribution
plt.hist(revenues, bins, color='r', alpha=0.5, label='revenue')
plt.xlabel('Amount(ETH)')
plt.ylabel('Number of Arbitrage Txs')
plt.legend()
plt.savefig('reports/revenue_dist.png')
plt.clf()

bins = []
start = 0
while start < 0.3:
    bins.append(start)
    start += 0.01
bins = np.array(bins)

# cost distribution
plt.hist(costs, bins, color='g', alpha=0.5, label='cost')
plt.xlabel('Amount(ETH)')
plt.ylabel('Number of Arbitrage Txs')
plt.legend()
plt.savefig('reports/cost_dist.png')
