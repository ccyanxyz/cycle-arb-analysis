import json
from common import *

swap_topic = "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822"
sync_topic = "0x1c411e9a96e071241c2f21f7726b17ae89e3cab4c78be50e062b03a9fffbbad1"
c = w3.eth.contract(abi=pairABI)

def to_log_receipt(l):
    l['blockHash'] = bytes.fromhex(l['blockHash'][2:])
    l['blockNumber'] = l['blockNumber'] #int(l['blockNumber'], 16)
    l['transactionIndex'] = l['transactionIndex'] #int(l['transactionIndex'], 16)
    l['transactionHash'] = bytes.fromhex(l['transactionHash'][2:])
    l['logIndex'] = l['logIndex'] #int(l['logIndex'], 16)
    l['address'] = w3.toChecksumAddress(l['address'])
    l['topics'] = [bytes.fromhex(t[2:]) for t in l['topics']]
    l['data'] = bytes.fromhex(l['data'][2:])
    return l

pairs = []
pairs_dict = {}
tx_dict = {}
stats = {}
def to_dict(pairs):
    d = {}
    for i in range(len(pairs)):
        d[pairs[i]['id']] = i
    return d

def parse_reserves(receipt):
    if len(receipt['logs']) <= 1:
        return False, None
    flag = False
    pair_revs = {}
    pair_addrs = []
    for log in receipt['logs']:
        if not len(log['topics']) or not log['topics'][0] == sync_topic:
            continue
        pair = None
        # addr = w3.toChecksumAddress(log['address'])
        addr = log['address']
        try:
            pair = pairs[pairs_dict[addr.lower()]]
        except:
            pass
        if not pair:
            continue
        l = to_log_receipt(log.copy())
        event = c.events.Sync().processLog(l)
        pair['reserve0'] = event['args']['reserve0']
        pair['reserve1'] = event['args']['reserve1']
        pair_revs[addr] = pair
        flag = True
    return flag, pair_revs

def main():
    stats = {0:{}}
    last_blk = 0
    count = 0
    sushi_start = 10794260
    with open('/data/receipts_export_new', 'r') as f:
        for line in f:
            info = json.loads(line)
            r = info['receipt']
            blockNumber = int(r['blockNumber'], 16)
            print(blockNumber, count)
            if blockNumber < sushi_start:
                continue
            if blockNumber > last_blk:
                with open('data/sushi_blockwise_reserves', 'a') as f1:
                    f1.write(json.dumps(stats)+'\n')
                stats = {}
                stats[blockNumber] = {}
                last_blk = blockNumber
            flag, pair_revs = parse_reserves(r)
            if not flag:
                continue
            count += 1
            for addr in pair_revs.keys():
                stats[blockNumber][addr] = pair_revs[addr]

if __name__ == '__main__':
    pairs = json.load(open('data/sushi_pairs.json'))
    pairs_dict = to_dict(pairs)
    main()
