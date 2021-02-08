import json
from web3.auto import w3

pairs = json.load(open('data/pairs.json'))
sushi_pairs = json.load(open('data/sushi_pairs.json'))

def get_pair(token0, token1):
    for pair in pairs:
        if token0 == pair['token0']['id'].lower() and token1 == pair['token1']['id'].lower():
            return pair['id']
        if token1 == pair['token0']['id'].lower() and token0 == pair['token1']['id'].lower():
            return pair['id']
    return None

def get_sushi_pair(token0, token1):
    for pair in sushi_pairs:
        if token0 == pair['token0']['id'] and token1 == pair['token1']['id']:
            return pair['id']
        if token1 == pair['token0']['id'] and token0 == pair['token1']['id']:
            return pair['id']
    return None

token2addr = {'WBTC':'0x2260fac5e5542a773aa44fbcfedf7c193bc2c599', 'USDC':'0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 'DAI':'0x6b175474e89094c44da98b954eedeac495271d0f', 'USDT':'0xdac17f958d2ee523a2206206994597c13d831ec7', 'YFI':'0x0bc529c00c6401aef6d220be8c6ea1667f6ad93e', 'LINK':'0x514910771af9ca656af840dff83e8264ecf986ca', 'SNX':'0xc011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f', 'BADGER':'0x3472a5a71965499acd81997a54bba8d852c6e53d', 'LON':'0x0000000000095413afc295d19edeb1ad7b71c952', 'DIGG':'0x798d1be841a82a273720ce31c822c61a67a601c3', 'UNI':'0x1f9840a85d5af5bf1d1762f925bdaddc4201f984', 'COMP':'0xc00e94cb662c3520282e6f5717214004a7f26888', 'sUSD':'0x57ab1ec28d129707052df4df418d58a2d46d5f51', 'MKR':'0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2', 'KP3R':'0x1ceb5cb57c4d4e2b2433641b95dd330a33185a44', 'WETH':'0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'}
# counts = json.load(open('data/path_counts.json'))
# top10 = list(counts.keys())[:10]
top10 = ['WBTC-ETH',
'USDC-ETH',
'DAI-ETH',
'ETH-USDT',
'YFI-ETH',
'LINK-ETH',
# 'AAVE-ETH',
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
    t0 = token2addr[token0]
    t1 = token2addr[token1]
    pair1 = get_pair(t0, t1)
    top10_path_pair_addrs.append(pair1)
    addr2symbols[pair1] = path

    pair2 = get_sushi_pair(t0, t1)
    pair2 = w3.toChecksumAddress(pair2)
    sushi_top10_path_pair_addrs.append(pair2)
    addr2symbols[pair2] = path
    symbol2addrs[path] = {'uni': pair1, 'sushi': pair2}
    print(path, pair1, pair2)
print(addr2symbols)

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
                    stats[name][i] = stats[name][str(bn-1)]
                except:
                    pass
        for addr in info[blockNumber].keys():
            ca = w3.toChecksumAddress(addr)
            r0 = info[blockNumber][addr]['reserve0']
            r1 = info[blockNumber][addr]['reserve1']
            if ca in top10_path_pair_addrs:
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
        for addr in sushi_top10_path_pair_addrs:
            name = addr2symbols[addr]
            if bn == 10000835 or bn == 0:
                sushi_stats[name][blockNumber] = {'r0': 0, 'r1': 0}
            else:
                try:
                    sushi_stats[name][i] = sushi_stats[name][str(bn-1)]
                except:
                    pass
        for addr in info[blockNumber].keys():
            ca = w3.toChecksumAddress(addr)
            r0 = info[blockNumber][addr]['reserve0']
            r1 = info[blockNumber][addr]['reserve1']
            if ca in sushi_top10_path_pair_addrs:
                name_ = addr2symbols[ca]
                sushi_stats[name_][bn] = {'r0': r0, 'r1': r1}
        idx += 1
json.dump(sushi_stats, open('data/sushi_10pair_blockwise_reserves.json', 'w'))
