import json
import time
from common import *

sync_topic = "0x1c411e9a96e071241c2f21f7726b17ae89e3cab4c78be50e062b03a9fffbbad1"
swap_topic = "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822"
mint_topic = "0x4c209b5fc8ad50758f13e2e1088ba56a560dff690a1c6fef26394f4c03821c4f"
burn_topic = "0xdccd412f0b1252819cb1fd330b93224ca42612892bb3f4f789976e6d81936496"
c = w3.eth.contract(abi=pairABI)

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

uni_pairs = []
sushi_pairs = []
uni_dict = {}
sushi_dict = {}
pairs = []
pairs_dict = {}
def to_dict(pairs):
    d = {}
    for i in range(len(pairs)):
        d[pairs[i]['id']] = i
    return d

def parse_cycle_arb(info):
    receipt = info['receipt']
    if len(receipt['logs']) <= 1:
        return None
    path = []
    amounts = []
    path_pairs = []
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
        path_pairs.append(pair)
        l = to_log_receipt(log.copy())
        event = c.events.Swap().processLog(l)
        input_token = pair['token0']['id']
        input_amount = event['args']['amount0In']
        output_token = pair['token1']['id']
        output_amount = event['args']['amount1Out']
        if event['args']['amount1In'] > 0:
            input_token = pair['token1']['id']
            input_amount = event['args']['amount1In']
            output_token = pair['token0']['id']
            output_amount = event['args']['amount0Out']
        path.append(input_token)
        amounts.append(input_amount)
        path.append(output_token)
        amounts.append(output_amount)
    if len(path) >= 3 and path[0] == path[-1]:
        revenue = amounts[-1] - amounts[0]
        tx = info['tx']
        cost = int(tx['gasPrice'], 16)*int(receipt['gasUsed'], 16)
        return { 'tx': tx, 'receipt': receipt, 'path': path, 'amounts': amounts, 'revenue': revenue, 'cost': cost, 'path_pairs': path_pairs }
    return None

def is_cross_arb(path_pairs):
    flag1 = False
    flag2 = False
    for p in path_pairs:
        if p in list(uni_dict.keys()):
            flag1 = True
        if p in list(sushi_dict.keys()):
            flag2 = True
        if flag1 and flag2:
            return True
    return False

def process_receipts():
    with open('/data/receipts_export_new', 'r') as f:
        idx = 0
        # for _ in range(6357186):
            # idx += 1
            # next(f)
        count = 0
        for line in f:
            info = json.loads(line)
            r = info['receipt']
            if int(r['blockNumber'], 16) < 10794229:
                continue
            print('block: ', int(r['blockNumber'], 16), '/ 11709847', 'line:', idx, 'count:', count)
            idx += 1
            ret = parse_cycle_arb(info)
            if not ret:
                continue
            if not is_cross_arb(ret['path_pairs']):
                continue
            count += 1
            with open('/data/cross_arb', 'a') as f1:
                f1.write(json.dumps(ret)+"\n")

if __name__ == '__main__':
    uni_pairs = json.load(open('data/pairs.json'))
    uni_dict = to_dict(uni_pairs)
    sushi_pairs = json.load(open('data/sushi_pairs.json'))
    sushi_dict = to_dict(sushi_pairs)
    pairs = []
    pairs.extend(uni_pairs)
    pairs.extend(sushi_pairs)
    pairs_dict = to_dict(pairs)
    process_receipts()
