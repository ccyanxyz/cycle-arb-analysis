from web3 import HTTPProvider, Web3
from web3.providers.ipc import IPCProvider
from web3._utils.request import make_post_request
from web3._utils.threads import Timeout
from json import JSONDecodeError
import json
from web3.auto import w3 as w3_rpc
from eth_abi import decode_abi
import socket
import requests

def generate_json_rpc(method, params, request_id=1):
    return {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': request_id,
    }

def generate_parity_get_receipts_rpc(blockNumber):
    return generate_json_rpc('parity_getBlockReceipts', [hex(blockNumber)])

def get_receipts_parity(blockNumber):
    headers = {
        'Content-Type': 'application/json',
    }
    rpc = generate_json_rpc('parity_getBlockReceipts', [hex(blockNumber)])
    data = json.dumps(rpc)
    data = data.encode('utf-8')
    ret = requests.post('http://localhost:8545', headers=headers, data=data)
    ret = json.loads(ret.text)
    return rpc_response_to_result(ret)

def generate_get_block_by_number_json_rpc(block_numbers, include_transactions):
    for idx, block_number in enumerate(block_numbers):
        yield generate_json_rpc(
            method='eth_getBlockByNumber',
            params=[hex(block_number), include_transactions],
            request_id=idx
        )

def generate_get_reserves_json_rpc(pairs, blockNumber='latest'):
    pairABI = json.load(open('abi/IUniswapV2Pair.json'))['abi']
    c = w3_rpc.eth.contract(abi=pairABI) 
    for pair in pairs:
        yield generate_json_rpc(
                method='eth_call',
                params=[{
                    'to': pair['address'],
                    'data': c.encodeABI(fn_name='getReserves', args=[]),
                    },
                    hex(blockNumber) if blockNumber != 'latest' else 'latest',
                    ]
                )

def generate_get_receipt_json_rpc(transaction_hashes):
    for idx, transaction_hash in enumerate(transaction_hashes):
        yield generate_json_rpc(
            method='eth_getTransactionReceipt',
            params=[transaction_hash],
            request_id=idx
        )

def rpc_response_batch_to_results(response):
    for response_item in response:
        yield rpc_response_to_result(response_item)


def rpc_response_to_result(response):
    result = response.get('result')
    if result is None:
        error_message = 'result is None in response {}.'.format(response)
        if response.get('error') is None:
            error_message = error_message + ' Make sure Ethereum node is synced.'
            # When nodes are behind a load balancer it makes sense to retry the request in hopes it will go to other,
            # synced node
            raise RetriableValueError(error_message)
        elif response.get('error') is not None and is_retriable_error(response.get('error').get('code')):
            raise RetriableValueError(error_message)
        raise ValueError(error_message)
    return result

class BatchHTTPProvider(HTTPProvider):

    def make_batch_request(self, text):
        self.logger.debug("Making request HTTP. URI: %s, Request: %s",
                          self.endpoint_uri, text)
        request_data = text.encode('utf-8')
        raw_response = make_post_request(
            self.endpoint_uri,
            request_data,
            **self.get_request_kwargs()
        )
        response = self.decode_rpc_response(raw_response)
        self.logger.debug("Getting response HTTP. URI: %s, "
                          "Requgst: %s, Response: %s",
                          self.endpoint_uri, text, response)
        return response

def has_valid_json_rpc_ending(raw_response: bytes) -> bool:
    stripped_raw_response = raw_response.rstrip()
    for valid_ending in [b"}", b"]"]:
        if stripped_raw_response.endswith(valid_ending):
            return True
    else:
        return False

class BatchIPCProvider(IPCProvider):

    def make_batch_request(self, text):
        self.logger.debug("Making request IPC")
        req_data = text.encode('utf-8')
        
        with self._lock, self._socket as sock:
            try:
                sock.sendall(req_data)
            except BrokenPipeError:
                sock = self._socket.reset()
                sock.sendall(req_data)

            raw_resp = b""
            with Timeout(self.timeout) as timeout:
                while True:
                    try:
                        raw_resp += sock.recv(512)
                    except socket.timeout:
                        timeout.sleep(0)
                        continue
                    if raw_resp == b"":
                        timeout.sleep(0)
                    elif has_valid_json_rpc_ending(raw_resp):
                        try:
                            resp = self.decode_rpc_response(raw_resp)
                        except JSONDecodeError:
                            timeout.sleep(0)
                            continue
                        else:
                            return resp
                    else:
                        timeout.sleep(0)
                        continue

class Client:
    def __init__(self, provider):
        self.w3 = Web3(provider)
        self.provider = provider

    def get_receipts(self, blockNumber='latest'):
        block = self.w3.eth.getBlock(blockNumber)
        txhashes = [t.hex() for t in block['transactions']]
        receipts_rpc = list(generate_get_receipt_json_rpc(txhashes))
        resp = self.provider.make_batch_request(json.dumps(receipts_rpc))
        results = list(rpc_response_batch_to_results(resp))
        return list(results)

    def get_reserves(self, pairs, blockNumber='latest'):
        r = list(generate_get_reserves_json_rpc(pairs, blockNumber))
        resp = self.provider.make_batch_request(json.dumps(r))
        results = list(rpc_response_batch_to_results(resp))
        for i in range(len(results)):
            res = decode_abi(['uint256', 'uint256', 'uint256'], bytes.fromhex(results[i][2:]))
            pairs[i]['reserve0'] = res[0]
            pairs[i]['reserve1'] = res[1]
        return pairs
