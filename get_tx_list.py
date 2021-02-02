import json
import requests

url = "https://api.etherscan.io/api?module=account&action=txlist&address=0xbb41594c19667b5054d2f501b82f768fb22777d5&startblock=0&endblock=99999999&sort=asc&apikey=SAWPNIM5KKPSQXRS28YA12B25SU1E3D3IF"

ret = requests.get(url)
j = ret.json()
print(list(j.keys()))
print(len(j['result']))

url = "https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock={start}&endblock={end}&sort=asc&apikey=SAWPNIM5KKPSQXRS28YA12B25SU1E3D3IF"
def get_tx_list(addr):

