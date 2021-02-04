import json

pairs = json.load(open('data/pairs.json'))

def get_pair(token0, token1):
    for pair in pairs:
        if token0 == pair['token0']['address'] and token1 == pair['token1']['address']:
            return pair['address']
        if token1 == pair['token0']['address'] and token0 == pair['token1']['address']:
            return pair['address']
    return None

counts = json.load(open('data/path_counts.json'))
top10 = list(counts.keys())[:10]
top10_path = {}
for path in top10:
    addrs = path.split('-')
    token0 = addrs[0]
    token1 = addrs[2]
    token2 = addrs[4]
    token0, token1, token2 = sorted([token0, token1, token2])
    pair1 = get_pair(token0, token1)
    pair2 = get_pair(token0, token2)
    pair3 = get_pair(token1, token2)
    top10_path[path] = {'tokens': [token0, token1, token2], 'pairs': [pair1, pair2, pair3]}

blockwise_reserves = json.load(open('data/toppair_blockwise_reserves.json'))
stats = {}
for path in top10:
    pair1 = top10_path[path]['pairs'][0]
    pair2 = top10_path[path]['pairs'][1]
    pair3 = top10_path[path]['pairs'][2]
    stats[path] = {}
    for bn in blockwise_reserves[pair1].keys():
        pr1 = blockwise_reserves[pair1][bn]
        pr2 = blockwise_reserves[pair2][bn]
        pr3 = blockwise_reserves[pair3][bn]
        # token0/token1 * token2/token0 * token1/token2
        arbidx = pr1['r0'] / pr1['r1'] * pr2['r1'] / pr2['r0'] * pr3['r0'] / pr3['r1']
        stats[path][bn] = arbidx
json.dump(stats, open('data/toppair_blockwise_arb_index.json', 'w'))
