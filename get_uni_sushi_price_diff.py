import json

pairs = json.load(open('data/pairs.json'))
sushi_pairs = json.load(open('data/sushi_pairs.json'))

def get_pair(token0, token1):
    for pair in pairs:
        if token0 == pair['token0']['id'] and token1 == pair['token1']['id']:
            return pair['id']
        if token1 == pair['token0']['id'] and token0 == pair['token1']['id']:
            return pair['id']
    return None

def get_sushi_pair(token0, token1):
    for pair in sushi_pairs:
        if token0 == pair['token0']['id'] and token1 == pair['token1']['id']:
            return pair['id']
        if token1 == pair['token0']['id'] and token0 == pair['token1']['id']:
            return pair['id']
    return None

# counts = json.load(open('data/path_counts.json'))
# top10 = list(counts.keys())[:10]
top10 = ['WBTC-ETH',
'USDC-ETH',
'DAI-ETH',
'ETH-USDT',
'YFI-ETH',
'LINK-ETH',
'AAVE-ETH',
'SNX-ETH',
'WBTC-BADGER',
'LON-USDT',
'WBTC-DIGG',
'UNI-ETH',
'COMP-ETH',
'sUSD-ETH',
'MKR-ETH',
'KP3R-ETH']
symbol2addrs = {}
addr2symbols = {}
top10_path_pairs = []
top10_path_pair_addrs = []
sushi_top10_path_pair_addrs = []
for path in top10:
    addrs = path.split('-')
    token0 = addrs[0]
    if token0 == 'ETH':
        token0 = 'WETH'
    token1 = addrs[1]
    if token1 == 'ETH':
        token1 = 'WETH'
    pair1 = get_pair(token0, token1)
    top10_path_pair_addrs.append(pair1)
    addr2symbols[pair1] = path

    pair2 = get_sushi_pair(token0, token1)
    sushi_top10_path_pair_addrs.append(pair2)
    addr2symbols[pair2] = path
    symbol2addrs[path] = {'uni': pair1, 'sushi': pair2}

stats = {}
for symbol in top10:
    stats[symbol] = {}
with open('data/blockwise_reserves', 'r') as f:
    idx = 0
    for line in f:
        info = json.loads(line)
        blockNumber = list(info.keys())[0]
        bn = int(blockNumber)
        print(bn)
        for addr in top10_path_pair_addrs:
            name = addr2symbols[addr]
            if bn == 10000835 or bn == 0:
                stats[name][blockNumber] = {'r0': 0, 'r1': 0}
            else:
                try:
                    stats[name][i] = stats[addr][str(bn-1)]
                except:
                    pass
        for addr in info[blockNumber].keys():
            r0 = info[blockNumber][addr]['reserve0']
            r1 = info[blockNumber][addr]['reserve1']
            if addr in top10_path_pair_addrs:
                name_ = addr2symbols[addr]
                stats[name_][bn] = {'r0': r0, 'r1': r1}
        idx += 1
json.dump(stats, open('data/10pair_blockwise_reserves.json', 'w'))

sushi_stats = {}
for symbol in top10:
    sushi_stats[symbol] = {}
with open('data/sushi_blockwise_reserves', 'r') as f:
    idx = 0
    for line in f:
        info = json.loads(line)
        blockNumber = list(info.keys())[0]
        bn = int(blockNumber)
        print('sushi', bn)
        name = addr2symbols[addr]
        for addr in sushi_top10_path_pair_addrs:
            if bn == 10000835 or bn == 0:
                sushi_stats[name][blockNumber] = {'r0': 0, 'r1': 0}
            else:
                try:
                    sushi_stats[name][i] = stats[addr][str(bn-1)]
                except:
                    pass
        for addr in info[blockNumber].keys():
            r0 = info[blockNumber][addr]['reserve0']
            r1 = info[blockNumber][addr]['reserve1']
            if addr in sushi_top10_path_pair_addrs:
                name_ = addr2symbols[addr]
                sushi_stats[name_][bn] = {'r0': r0, 'r1': r1}
        idx += 1
json.dump(stats, open('data/sushi_10pair_blockwise_reserves.json', 'w'))
