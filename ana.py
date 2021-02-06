import json
from web3 import Web3
from web3.providers.rpc import HTTPProvider
from web3.providers.ipc import IPCProvider
from web3 import WebsocketProvider

sync_topic = "0x1c411e9a96e071241c2f21f7726b17ae89e3cab4c78be50e062b03a9fffbbad1"
swap_topic = "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822"
mint_topic = "0x4c209b5fc8ad50758f13e2e1088ba56a560dff690a1c6fef26394f4c03821c4f"
burn_topic = "0xdccd412f0b1252819cb1fd330b93224ca42612892bb3f4f789976e6d81936496"
w3 = Web3()
pairABI = json.load(open('IUniswapV2Pair.json'))['abi']
erc20abi = json.load(open('erc20.abi'))
c = w3.eth.contract(abi=pairABI)
def to_dict(pairs):
    d = {}
    for i in range(len(pairs)):
        d[pairs[i]['id']] = i
    return d

def to_log_receipt(l):
    l['blockHash'] = bytes.fromhex(l['blockHash'][2:])
    l['blockNumber'] = int(l['blockNumber'], 16)
    l['transactionIndex'] = int(l['transactionIndex'], 16)
    l['transactionHash'] = bytes.fromhex(l['transactionHash'][2:])
    l['logIndex'] = int(l['logIndex'], 16)
    l['address'] = w3.toChecksumAddress(l['address'])
    l['topics'] = [bytes.fromhex(t[2:]) for t in l['topics']]
    l['data'] = bytes.fromhex(l['data'][2:])
    return l

def to_tx_receipt(r):
    r['blockHash'] = None if not r['blockHash'] else bytes.fromhex(r['blockHash'][2:])
    r['blockNumber'] = None if not r['blockNumber'] else int(r['blockNumber'], 16)
    r['transactionIndex'] = None if not r['transactionIndex'] else int(r['transactionIndex'], 16)
    r['transactionHash'] = bytes.fromhex(r['transactionHash'][2:])
    r['cumulativeGasUsed'] = int(r['cumulativeGasUsed'], 16)
    r['status'] = int(r['status'], 16)
    r['gasUsed'] = int(r['gasUsed'], 16)
    r['contractAddress'] = None if not r['contractAddress'] else w3.toChecksumAddress(r['contractAddress'])
    r['logs'] = [to_log_receipt(t) for t in r['logs']]
    r['logsBloom'] = bytes.fromhex(r['logsBloom'][2:])
    r['from'] = None if not r['from'] else w3.toChecksumAddress(r['from'])
    r['to'] = w3.toChecksumAddress(r['to'])
    return r

pairs = json.load(open('pairs.json'))
pairs_dict = to_dict(pairs)
def to_dict(pairs):
    d = {}
    for i in range(len(pairs)):
        d[pairs[i]['id']] = i
    return d

file = open('cycle_include_router.json')
stats = {'before' : [], 'after' : []}
k = 0
for line in file.readlines():
    print(k)
    k = k + 1
    info = json.loads(line)
    receipt = info['receipt']
    reserve = []
    for log in receipt['logs']:
        if not len(log['topics']) or not log['topics'][0] == sync_topic:
            continue
        pair = None
        addr = w3.toChecksumAddress(log['address'])
        try:
            pair = pairs[pairs_dict[addr]]
        except Exception as e:
            pass
        if not pair:
            continue
        l = to_log_receipt(log.copy())
        event = c.events.Sync().processLog(l)
        reserve.append([event['args']['reserve0'], event['args']['reserve1']])
        #input_token = pair['token0']['id']
        #input_amount = event['args']['amount0In']
        #output_token = pair['token1']['id']
        #output_amount = event['args']['amount1Out']
        #print(input_amount, output_amount)
    i = 0
    ori_rate = 1
    new_rate = 1
    for log in receipt['logs']:
        if not len(log['topics']) or not log['topics'][0] == swap_topic:
            continue
        pair = None
        addr = w3.toChecksumAddress(log['address'])
        try:
            pair = pairs[pairs_dict[addr]]
        except Exception as e:
            pass
        if not pair:
            continue
        l = to_log_receipt(log.copy())
        event = c.events.Swap().processLog(l)
        input_token = pair['token0']['id']
        input_amount = event['args']['amount0In']
        output_token = pair['token1']['id']
        output_amount = event['args']['amount1Out']
        if input_amount == 0:
            input_amount = event['args']['amount1In'] / pow(10, int(pair['token1']['decimals']))
            output_amount = event['args']['amount0Out'] / pow(10, int(pair['token0']['decimals']))
            reserve[i][0] = reserve[i][0] / pow(10, int(pair['token0']['decimals']))
            reserve[i][1] = reserve[i][1] / pow(10, int(pair['token1']['decimals']))
            ori_rate = ori_rate * (reserve[i][1] / reserve[i][0])
            new_rate = new_rate * ((reserve[i][1] - input_amount) / (reserve[i][0] + output_amount))
        else:
            input_amount = event['args']['amount0In'] / pow(10, int(pair['token0']['decimals']))
            output_amount = event['args']['amount1Out'] / pow(10, int(pair['token1']['decimals']))
            reserve[i][0] = reserve[i][0] / pow(10, int(pair['token0']['decimals']))
            reserve[i][1] = reserve[i][1] / pow(10, int(pair['token1']['decimals']))
            ori_rate = ori_rate * (reserve[i][0] / reserve[i][1])
            new_rate = new_rate * ((reserve[i][0] - input_amount) / (reserve[i][1] + output_amount))
        i = i + 1
    stats['before'].append(new_rate)
    stats['after'].append(ori_rate)

json.dump(stats, open('beforeafter.json', 'w'))