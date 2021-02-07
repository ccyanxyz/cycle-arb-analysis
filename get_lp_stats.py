import json
from web3 import Web3
from datetime import datetime
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
erc20 = w3.eth.contract(abi=erc20abi)
ts = json.load(open('ts.json'))

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


f = open('/data/receipts_export_new')
stats = {'0xe2aab7232a9545f29112f9e6441661fd6eeb0a5d' : {}, '0x97524f602706cdb64f9dfa71909ace06e98200b6' : {}, '0xaf996125e98b5804c00ffdb4f7ff386307c99a00' : {}, '0x1273ad5d8f3596a7a39efdb5a4b8f82e8f003fc3' : {}, '0x724d5c9c618a2152e99a45649a3b8cf198321f46' : {}, '0x6deb633e4441b8879aff48caa6e021e919ddbb0c' : {}}
k = 0
for line in f:
    info = json.loads(line)
    receipt = info['receipt']
    bn = int(info['receipt']['blockNumber'], 16)
    print(bn)
    t = ts[str(bn)]
    d = datetime.utcfromtimestamp(t).strftime('%Y-%m-%d')
    for pair in stats.keys():
        if d not in stats[pair].keys():
            stats[pair][d] = 0
    for i in range(len(receipt['logs'])):
        if receipt['logs'][i]['topics'][0] == mint_topic:
            addr = str.lower(w3.toChecksumAddress(receipt['logs'][i]['address']))
            if addr in stats.keys():
                for j in reversed(range(i)):
                    if str.lower(w3.toChecksumAddress(receipt['logs'][i]['address'])) != addr:
                        continue
                    l = to_log_receipt(receipt['logs'][j].copy())
                    event = erc20.events.Transfer().processLog(l)
                    if 'from' in event['args'].keys() and event['args']['from'] == '0x0000000000000000000000000000000000000000' and event['args']['to'] != '0x0000000000000000000000000000000000000000':
                        stats[addr][d] += event['args']['value']
                        break
        if receipt['logs'][i]['topics'][0] == burn_topic:
            addr = str.lower(w3.toChecksumAddress(receipt['logs'][i]['address']))
            if addr in stats.keys():
                for j in reversed(range(i)):
                    if str.lower(w3.toChecksumAddress(receipt['logs'][i]['address'])) != addr:
                        continue
                    l = to_log_receipt(receipt['logs'][j].copy())
                    event = erc20.events.Transfer().processLog(l)
                    if 'from' in event['args'].keys() and event['args']['from'] != '0x0000000000000000000000000000000000000000' and event['args']['to'] == '0x0000000000000000000000000000000000000000':
                        stats[addr][d] = stats[addr][d] - event['args']['value']
                        break

json.dump(stats, open('lp_stats.json', 'w'))
