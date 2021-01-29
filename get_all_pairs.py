import json
from common import w3, erc20abi, uni

def getAllPairs(pair_file):
    uni.set_block_number(11709847)
    num = uni.get_num_pairs()
    print(num)
    pairs = json.load(open(pair_file))
    start = 0
    if len(pairs) > 0:
        start = pairs[-1]['index'] + 1
    for i in range(start, num):
        addr = uni.get_pair_by_index(i)
        try:
            token0 = uni.get_token_0(addr)
            token1 = uni.get_token_1(addr)
        except Exception as e:
            print('get_token_0/1 error:', e)
            raise
            continue
        try:
            erc20 = w3.eth.contract(address=token0, abi=erc20abi)
            symbol0 = erc20.functions.symbol().call()
            decimal0 = erc20.functions.decimals().call()
        except Exception as e:
            print('get symbol0 error:', e)
            continue
        try:
            erc20 = w3.eth.contract(address=token1, abi=erc20abi)
            symbol1 = erc20.functions.symbol().call()
            decimal1 = erc20.functions.decimals().call()
        except Exception as e:
            print('get symbol1 error:', e)
            continue
        try:
            reserves = uni.get_reserves(addr)
        except Exception as e:
            print('get_reserves error:', e)
            continue

        pair = {
                'index': i,
                'address': addr,
                'token0': {
                    'address': token0,
                    'symbol': symbol0,
                    'decimal': decimal0,
                    },
                'token1': {
                    'address': token1,
                    'symbol': symbol1,
                    'decimal': decimal1,
                    },
                'reserve0': reserves[0],
                'reserve1': reserves[1],
                }
        print(i, '/', num, pair)
        pairs.append(pair)
        if i % 5 == 0:
            json.dump(pairs, open(pair_file, 'w'))
    json.dump(pairs, open(pair_file, 'w'))

if __name__ == '__main__':
    getAllPairs('data/pairs.json')
