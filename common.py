import json
import requests
from web3 import Web3
from web3.providers.rpc import HTTPProvider
from web3.providers.ipc import IPCProvider
from web3 import WebsocketProvider
from uniswap.uniswap import UniswapV2Client
from uniswap.uniswap import UniswapV2Utils as utils
from rpc import BatchHTTPProvider, BatchIPCProvider
import threading
import random

config = json.load(open('config.json'))
network = config['network']
address = config['address']
privkey = config['privkey']
http_addr = config[network]['http']
wss_addr = config[network]['wss']

uni = UniswapV2Client(address, privkey, http_addr)

# w3 = Web3(HTTPProvider(http_addr, request_kwargs={'timeout': 6000}))
w3 = Web3(IPCProvider('/data/geth/geth.ipc', timeout=6000))
ws = Web3(WebsocketProvider(wss_addr))
# batch_provider = BatchHTTPProvider(config[network]['http'])
batch_provider = BatchIPCProvider('/data/geth/geth.ipc', timeout = 6000)

pairABI = json.load(open('abi/IUniswapV2Pair.json'))['abi']
erc20abi = json.load(open('./abi/erc20.abi'))
