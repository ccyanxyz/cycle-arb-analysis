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
    g0 = iter(list(blockwise_reserves[pair1].keys()))
    g1 = iter(list(blockwise_reserves[pair2].keys()))
    g2 = iter(list(blockwise_reserves[pair3].keys()))
    l0, l1, l2 = list(blockwise_reserves[pair1].keys()), list(blockwise_reserves[pair2].keys()), list(blockwise_reserves[pair3].keys())
    idx0, idx1, idx2 = 0, 0, 0
    i0 = next(g0)
    i1 = next(g1)
    i2 = next(g2)
    start = max([i0, i1, i2])
    end = min([l0[-1], l1[-1], l2[-1]])
    print('start:', start, 'end:', end)
    for bn in range(start, end):
        while i0 < bn:
            if idx0 + 1 < len(l0) and l0[idx0+1] > bn:
                break
            i0 = next(g0)
            idx0 += 1
        while i1 < bn:
            if idx1 + 1 < len(l1) and l1[idx1+1] > bn:
                break
            i1 = next(g1)
            idx1 += 1
        while i2 < bn:
            if idx2 + 1 < len(l2) and l2[idx2+1] > bn:
                break
            i2 = next(g2)
            idx2 += 1
        pr1 = blockwise_reserves[pair1][str(i0)]
        pr2 = blockwise_reserves[pair2][str(i1)]
        pr3 = blockwise_reserves[pair3][str(i2)]
        # token0/token1 * token2/token0 * token1/token2
        arbidx = pr1['r0'] / pr1['r1'] * pr2['r1'] / pr2['r0'] * pr3['r0'] / pr3['r1']
        stats[path][bn] = arbidx
json.dump(stats, open('data/toppair_blockwise_arb_index.json', 'w'))
