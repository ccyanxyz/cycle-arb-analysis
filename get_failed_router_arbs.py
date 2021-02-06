import json
from web3.auto import w3

# need to identify if its a cycle tx or not
router_abi = json.load(open('abi/UniswapV2Router02.json'))
router = w3.eth.contract(address=w3.toChecksumAddress("0x7a250d5630b4cf539739df2c5dacb4c659f2488d"), abi=router_abi)

def is_cycle(info):
    try:
        return info['path'][0] == info['path'][-1] and len(info['path']) >= 4
    except:
        return False

with open('/data/tx_info/0x7a250d5630b4cf539739df2c5dacb4c659f2488d') as f:
# with open('data/0x7a250d5630b4cf539739df2c5dacb4c659f2488d') as f:
    idx = 0
    for line in f:
        print(idx)
        idx += 1
        l = json.loads(line)
        if l['txreceipt_status'] == 1:
            continue
        try:
            info = router.decode_function_input(l['input'])
        except:
            continue
        if not is_cycle(info[1]):
            continue
        with open('data/failed_router_arbs.json', 'a') as f1:
            f1.write(json.dumps(l)+'\n')
