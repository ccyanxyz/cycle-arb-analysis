# from etherscan.accounts import Account
import json
import requests
import os

# url = "https://api.etherscan.io/api?module=account&action=txlist&address=0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D&startblock=10207858&endblock=10208858&sort=asc&apikey=SAWPNIM5KKPSQXRS28YA12B25SU1E3D3IF"

# ret = requests.get(url)
# j = ret.json()
# print(list(j.keys()))
# print(len(j['result']))

# address = "0x3930f8809fD21dc3EC725a92F16D5468ebf27e88"
# api = Account(address=address, api_key="SAWPNIM5KKPSQXRS28YA12B25SU1E3D3IF")
# txs = api.get_all_transactions(offset=1000, sort='asc', internal=False)
# print(len(txs))
# print(txs[0])

url = "https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock={start}&endblock={end}&sort=asc&apikey=SAWPNIM5KKPSQXRS28YA12B25SU1E3D3IF"
def get_tx_list(address):
    start = 10000835
    end = 11709847

    current = 10000835
    step = 10000
    count = 0
    while current < end:
        u = url.replace('{address}', address).replace('{start}', str(current)).replace('{end}', str(current+step))
        try:
            ret = requests.get(u)
            data = ret.json()
        except:
            continue
        if len(data['result']) >= 10000:
            step = int(step/2)
            continue
        print('current_block:', current, 'count:', count)
        current += step
        step = int(step*2)
        count += len(data['result'])
        for item in data['result']:
            with open('/data/tx_info/'+address, 'a') as f:
                f.write(json.dumps(item)+'\n')
    print('count:', count)
    return count

addrs = json.load(open('data/addrs.json'))
addrs.reverse()
counts = {}
l = os.listdir('/data/tx_info')
i = 0
for addr in addrs:
    i += 1
    print('address:', addr, i)
    if addr in l:
        continue
    count = get_tx_list(addr)
    counts[addr] = count
json.dump(counts, open('data/addr_tx_count.json', 'w'))
