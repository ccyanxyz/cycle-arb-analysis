import requests
import json

def get_query(skip):
    query = '''
    {
       pairs(first: 1000, skip: $skip) { 
        id
        token0 {
          id
          symbol
          decimals
        }
        token1 {
          id
          symbol
          decimals
        }
        reserve0
        reserve1
       }
    }'''
    return query.replace('$skip', str(skip))
url = "https://api.thegraph.com/subgraphs/name/croco-finance/sushiswap"

from gql import gql, Client
# from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.requests import RequestsHTTPTransport

# transport = AIOHTTPTransport(url="https://countries.trevorblades.com/")
transport = RequestsHTTPTransport(url=url)
client = Client(transport=transport, fetch_schema_from_transport=True)

all_pairs = []
query = gql(get_query(0))
result = client.execute(query)
all_pairs.extend(result['pairs'])
with open('data/sushi_pairs.json', 'w') as f:
    json.dump(all_pairs, f)
