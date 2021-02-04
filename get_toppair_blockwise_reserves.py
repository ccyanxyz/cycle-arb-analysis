import json

pairs = json.load(open('data/pairs.json'))

def get_pair(token0, token1):
    for pair in pairs:
        if token0 == pair['token0']['id'] and token1 == pair['token1']['id']:
            return pair['id']
        if token1 == pair['token0']['id'] and token0 == pair['token1']['id']:
            return pair['id']
    return None

counts = json.load(open('data/path_counts.json'))
top10 = list(counts.keys())[:10]
top10_path_pairs = []
top10_path_pair_addrs = []
for path in top10:
    addrs = path.split('-')
    token0 = addrs[0]
    token1 = addrs[2]
    token2 = addrs[4]
    pair1 = get_pair(token0, token1)
    pair2 = get_pair(token0, token2)
    pair3 = get_pair(token1, token2)
    top10_path_pair_addrs.append(pair1)
    top10_path_pair_addrs.append(pair2)
    top10_path_pair_addrs.append(pair3)

stats = {}
for addr in top10_path_pair_addrs:
    stats[addr] = {}
with open('data/blockwise_reserves', 'r') as f:
    idx = 0
    last_bn = 10000835
    for line in f:
        info = json.loads(line)
        blockNumber = list(info.keys())[0]
        bn = int(blockNumber)
        print(bn)
        for addr in top10_path_pair_addrs:
            if bn == 10000835 or bn == 0:
                stats[addr][blockNumber] = {'r0': 0, 'r1': 0}
            else:
                for i in range(last_bn+1, bn):
                    try:
                        stats[addr][i] = stats[addr][str(last_bn)]
                    except:
                        pass
        for addr in info[blockNumber].keys():
            r0 = info[blockNumber][addr]['reserve0']
            r1 = info[blockNumber][addr]['reserve1']
            if addr in top10_path_pair_addrs:
                stats[addr][bn] = {'r0': r0, 'r1': r1}
        idx += 1
        last_bn = bn
json.dump(stats, open('data/toppair_blockwise_reserves.json', 'w'))
