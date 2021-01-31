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
with open('../files/blockwise_reserves', 'r') as f:
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
                    stats[addr][blockNumber] = stats[addr][str(bn-1)]
                except:
                    pass
        for addr in info[blockNumber].keys():
            r0 = info[blockNumber][addr]['reserve0']
            r1 = info[blockNumber][addr]['reserve1']
            if addr in top10_path_pair_addrs:
                stats[addr][blockNumber] = {'r0': r0, 'r1': r1}
        idx += 1
json.dump(stats, open('data/blockwise_reserves.json', 'w'))

'''
ma_bot_profit_graph_lines = ""
for addr in top10:
    bot_profit_coords = ""
    bot_profit = [data[addr][k] for k in data[addr]]
    bot_profit_ma = get_moving_average(bot_profit, 7)
    i = 0
    for k in data[addr].keys():
        bot_profit_coords += "(%s,%f) " % (k, bot_profit_ma[i])
        i += 1
    ma_bot_profit_graph_lines += COORDS_CONSTANT.replace("%coords%", bot_profit_coords) + "\n"

top_bots = ['ETH-YAM-yCRV', 'ETH-XSP-XFI', 'ETH-XRT-RWS', 'ETH-YAM-yyCRV', 'ETH-XAMP-TOB', 'ETH-$BASED-sUSD', 'ETH-SWAP-HEX2T', 'ETH-YFBETA-YFARM', 'ETH-UniFi-buidl', 'ETH-XSP-USDT']
open('reports/top10_paths.tex', 'w').write(LINE_TEMPLATE.replace("%plots%", ma_bot_profit_graph_lines).replace("%legendkeys%", ",".join([x for x in top_bots])).replace("%title%", "Top 10 Ring Path Txs, 7-Day Moving Average").replace("%ylabel%", "Number of Txs").replace("%max%", str(2*5000)).replace("%legendpos%", "outer north east").replace("%extraaxisoptions%", ",enlarge x limits=-1,width=.9\\textwidth, height=0.4\\textwidth,x label style={at={(1.15,-.15)},anchor=south,}"))
'''
