# Uniswap Cycle Arbitrage Analysis

* Previous work on cycle arbitrage: https://github.com/ccyanxyz/uniswap-arbitrage-analysis
* General structure:

```
.
├── abi // smart contract ABI file
├── data // output data
├── go-ethereum // modified go-ethereum 
├── reports // data analysis results
├── template // latex figure templates
├── test // test scripts
├── uniswap-v2-py // uniswap v2 python client
└── utils // helper scripts
```

* Go-ethereum: this is a modified go-ethereum client allowing us to export all transactions and receipts related to uniswap/sushiswap, the output is a 22959997 line file, each line contains a transaction and the corresponding receipt, key modifications:
  * go-ethereum/core/blockchain.go: start from line 792, function ExportReceiptsN
  * go-ethereum/core/transaction.go: start from line 49, Txdata structure
* Key Python scripts:
  * get_all_pairs_thegraph.py: get all uniswap pairs via TheGraph API
  * get_all_cycle_arbs.py: identify and extract all successful cyclic arbitrages
  * count_cycles.py: count the cycle lengths
  * get_start_token_stats.py: count the start tokens for cyclic arbitrages
  * get_daily_revenue.py: get daily revenue of all cyclic arbitrages
  * get_gas_trend.py: get daily gas cost for cyclic arbitrages
  * get_profit_rev_dist.py: get profit/revenue distribution for cyclic arbitrages
  * get_bot_stats.py: get stats of cyclic arbitrage contracts
  * get_tx_list.py: get all transactions related to those arbitrage contracts we identified, including the UniswapV2Router contract
  * get_failed_stats.py: get stats of failed cyclic arbitrages excluding those initiated from the UniswapV2Router contract
  * get_failed_router_stats.py: get stats of all failed cyclic arbitrage transactions initiated from the UniswapV2Router contract
  * get_top10bot_daily_revenue.py: get the daily revenue stats of the top 10 bots in terms of total revenue
  * get_blockwise_stats.py: get blockwise reserves info of all uniswap pairs
  * get_toppair_blockwise_reserves.py: get the blockwise reserves of those pairs in the top 10 arbitrage path
  * draw_xxx.py: draw the analysis results with python matplotlib
  * tex_xxx.py: draw the analysis results with Latex templates

