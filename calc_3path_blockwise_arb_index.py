import json

pairs = json.load(open('data/pairs.json'))

def get_pair(token0, token1):
    for pair in pairs:
        if token0 == pair['token0']['id'] and token1 == pair['token1']['id']:
            return pair['id']
        if token1 == pair['token0']['id'] and token0 == pair['token1']['id']:
            return pair['id']
    return None

# counts = json.load(open('data/path_counts.json'))
# top10 = list(counts.keys())[:10]
top10 = ["0x0Ba45A8b5d5575935B8158a88C631E9F9C95a2e5-0x0Ba45A8b5d5575935B8158a88C631E9F9C95a2e5-0x6B175474E89094C44Da98b954EedeAC495271d0F-0x6B175474E89094C44Da98b954EedeAC495271d0F-0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2-0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2-", "0x327682779bAB2BF4d1337e8974ab9dE8275A7Ca8-0x327682779bAB2BF4d1337e8974ab9dE8275A7Ca8-0x0Ae055097C6d159879521C384F1D2123D1f195e6-0x0Ae055097C6d159879521C384F1D2123D1f195e6-0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2-0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2-", "0x27702a26126e0B3702af63Ee09aC4d1A084EF628-0x27702a26126e0B3702af63Ee09aC4d1A084EF628-0x6B175474E89094C44Da98b954EedeAC495271d0F-0x6B175474E89094C44Da98b954EedeAC495271d0F-0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2-0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2-"]
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

blockwise_reserves = json.load(open('data/3path_blockwise_reserves.json'))
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
    i0 = int(next(g0))
    if i0 == 0:
        i0 = int(next(g0))
        idx0 += 1
    i1 = int(next(g1))
    if i1 == 0:
        i1 = int(next(g1))
        idx1 += 1
    i2 = int(next(g2))
    if i2 == 0:
        i2 = int(next(g2))
        idx2 += 1
    start = int(max([i0, i1, i2]))
    end = int(min([l0[-1], l1[-1], l2[-1]]))
    print('start:', start, 'end:', end)
    for bn in range(start, end):
        while i0 < bn:
            if idx0 + 1 < len(l0) and int(l0[idx0+1]) > bn:
                break
            i0 = int(next(g0))
            idx0 += 1
        while i1 < bn:
            if idx1 + 1 < len(l1) and int(l1[idx1+1]) > bn:
                break
            i1 = int(next(g1))
            idx1 += 1
        while i2 < bn:
            if idx2 + 1 < len(l2) and int(l2[idx2+1]) > bn:
                break
            i2 = int(next(g2))
            idx2 += 1
        pr1 = blockwise_reserves[pair1][str(i0)]
        pr2 = blockwise_reserves[pair2][str(i1)]
        pr3 = blockwise_reserves[pair3][str(i2)]
        if pr1['r0'] * pr1['r1'] * pr2['r1'] * pr2['r0'] * pr3['r0'] * pr3['r1'] == 0:
            stats[path][bn] = 0
            continue
        # token0/token1 * token2/token0 * token1/token2
        arbidx = pr1['r0'] / pr1['r1'] * pr2['r1'] / pr2['r0'] * pr3['r0'] / pr3['r1']
        stats[path][bn] = arbidx
json.dump(stats, open('data/3path_blockwise_arb_index.json', 'w'))
