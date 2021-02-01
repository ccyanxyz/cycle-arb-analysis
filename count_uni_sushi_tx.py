import json

sushi_addresses = []
uni_addresses = []
def get_tx_info(info):
    receipt = info['receipt']
    if len(receipt['logs']) <= 1:
        return False, False
    is_sushi = False
    is_uni = False
    for log in receipt['logs']:
        if not len(log['topics']) or not log['topics'][0] == swap_topic:
            continue
        addr = w3.toChecksumAddress(log['address'])
        if addr in sushi_addresses:
            is_sushi = True
        if addr in uni_addresses:
            is_uni = True
        if is_sushi and is_uni:
            return True, True
    return is_uni, is_sushi

sushi_pairs = json.load(open('data/sushi_pairs.json'))
uni_pairs = json.load(open('data/pairs.json'))
sushi_addresses = [p['id'] for p in sushi_pairs]
uni_addresses = [p['id'] for p in uni_pairs]
uni_count = 0
sushi_count = 0
with open('/data/receipts_export_new', 'r') as f:
    for line in f:
        info = json.loads(line)
        print(int(info['receipt']['blockNumber'], 16))
        is_uni, is_sushi = get_tx_info(info)
        if is_uni:
            uni_count += 1
            with open('/data/uni_receipts', 'a') as f1:
                f1.write(json.dumps(info)+'\n')
        if is_sushi:
            sushi_count += 1
            with open('/data/sushi_receipts', 'a') as f2:
                f2.write(json.dumps(info)+'\n')
    print('uni:', uni_count, 'sushi:', sushi_count)
