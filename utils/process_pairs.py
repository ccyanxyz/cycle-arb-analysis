import json
from web3.auto import w3

pairs = json.load(open('data/pairs.json'))
for pair in pairs:
    pair['id'] = w3.toChecksumAddress(pair['id'])
    pair['token0']['id'] = w3.toChecksumAddress(pair['token0']['id'])
    pair['token1']['id'] = w3.toChecksumAddress(pair['token1']['id'])
json.dump(pairs, open('data/pairs1.json', 'w'))
