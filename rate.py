import numpy as np
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import json

stats = json.load(open('beforeafter.json'))
before = stats['before']
after = stats['after']

num = 0
num1 = 0
numb = 0

for i in range(len(before)):
    if before[i] == 0:
        print(i, after[i])
        numb = numb + 1
        continue
    if before[i] < 1:
        before[i] = 1 / before[i]
    if after[i] < 1:
        after[i] = 1 / after[i]
    if after[i] <= 1.01:
        num +=1
    if after[i] <= 1/0.997/0.997/0.997:
        num1 += 1
    if before[i] >= 1.1:
        numb = numb + 1

print(num, num1, numb, len(before))

start = 1
bins = []
while start <= 10:
    if start == 1.009:
        bins.append(1/0.997/0.997/0.997)
    else:
        bins.append(start)
    start = start + 0.001

plt.figure(figsize=(14, 5))
plt.hist(before, bins, color='b', alpha=0.5, label='before')
# revenue distribution
plt.hist(after, bins, color='r', alpha=0.5, label='after')
plt.xlabel('Arbitrage Index', fontsize=15)
plt.ylabel('Number of Arbitrage Txs', fontsize=15)
plt.legend()
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.vlines(1/0.997/0.997/0.997, 0, 100000, colors="b", linestyles="dashed")
plt.text(1.012, 50000, "minimum profitable arbitrage index = 1.009", ha='left', va='bottom', fontsize=15)
#plt.yscale('log')
#plt.ylim(0,60000)
plt.xlim(0.99, 1.1)
plt.savefig('rate.png')
plt.clf()