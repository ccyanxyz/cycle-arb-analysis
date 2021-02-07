import json
import threading
from common import *

pairs = {'0xe2aab7232a9545f29112f9e6441661fd6eeb0a5d' : 10888346, '0x97524f602706cdb64f9dfa71909ace06e98200b6' : 11381242 , '0xaf996125e98b5804c00ffdb4f7ff386307c99a00' : 10839738 , '0x1273ad5d8f3596a7a39efdb5a4b8f82e8f003fc3' : 10848938,  '0x724d5c9c618a2152e99a45649a3b8cf198321f46' : ,10794697  '0x6deb633e4441b8879aff48caa6e021e919ddbb0c' : 10401028}

stats = {}
for addr in pairs.keys():
    stats[addr] = {}
def get_lp_supply(addr, start):
    c = w3.eth.contract(address = w3.toChecksumAddress(addr), abi=erc20abi)
    for i in range(start, 11709847):
        ret = c.functions.totalSupply().call(block_identifier=i)
        print(addr, i, ret)
        stats[addr][i] = ret

threads = []
for addr in pairs.keys():
    t = threading.Thread(target=get_lp_supply, args=(addr, pairs[addr], ))
    threads.append(t)
for t in threads:
    t.start()
for t in threads:
    t.join()
