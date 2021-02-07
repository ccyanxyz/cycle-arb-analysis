import json

pairs = json.load(open('data/pairs.json'))

def get_pair(token0, token1):
    for pair in pairs:
        if token0 == pair['token0']['id'] and token1 == pair['token1']['id']:
            return pair['id']
        if token1 == pair['token0']['id'] and token0 == pair['token1']['id']:
            return pair['id']
    print(token0, token1, 'no pair')
    exit()
    return None

# counts = json.load(open('data/path_counts.json'))
# top10 = list(counts.keys())[:10]
# DAI-TRB-WETH, BPT-STA-WETH, ALEPH-DAI-WETH
top10 = ["0x0Ba45A8b5d5575935B8158a88C631E9F9C95a2e5-0x0Ba45A8b5d5575935B8158a88C631E9F9C95a2e5-0x6B175474E89094C44Da98b954EedeAC495271d0F-0x6B175474E89094C44Da98b954EedeAC495271d0F-0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2-0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2-", "0x0e511Aa1a137AaD267dfe3a6bFCa0b856C1a3682-0x0e511Aa1a137AaD267dfe3a6bFCa0b856C1a3682-0xa7DE087329BFcda5639247F96140f9DAbe3DeED1-0xa7DE087329BFcda5639247F96140f9DAbe3DeED1-0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2-0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2-", "0xC0134b5B924c2FCA106eFB33C45446c466FBe03e-0xC0134b5B924c2FCA106eFB33C45446c466FBe03e-0x6B175474E89094C44Da98b954EedeAC495271d0F-0x6B175474E89094C44Da98b954EedeAC495271d0F-0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2-0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2-"]
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
    for line in f:
        info = json.loads(line)
        blockNumber = list(info.keys())[0]
        bn = int(blockNumber)
        print(bn)
        for addr in top10_path_pair_addrs:
            if bn == 10000835 or bn == 0:
                stats[addr][blockNumber] = {'r0': 0, 'r1': 0}
            else:
                try:
                    stats[addr][i] = stats[addr][str(bn-1)]
                except:
                    pass
        for addr in info[blockNumber].keys():
            r0 = info[blockNumber][addr]['reserve0']
            r1 = info[blockNumber][addr]['reserve1']
            if addr in top10_path_pair_addrs:
                stats[addr][bn] = {'r0': r0, 'r1': r1}
        idx += 1
json.dump(stats, open('data/3path_blockwise_reserves.json', 'w'))
