import json

BREADTH_SCATTER_TEMPLATE = open('template/breadth.tex').read()
data = json.load(open('data/gas_trend.json'))

gas_usage_coords = ""
for k in data.keys():
    gas_usage_coords += "(%s,%f) [%f] " % (k, data[k]['mean_gas_used'], data[k]['mean_gas_price']/1e9)

open('reports/gas_trend.tex', 'w').write(BREADTH_SCATTER_TEMPLATE.replace("%coords%", gas_usage_coords).replace("%macoords%", "").replace("%title%", "Gas Trends in Ring Arbitrage").replace("%cumcoords%", "(2018-03-08, 0) (2018-03-08, 500000)").replace("%extra%", "").replace("%max%", "500000").replace("%ylabel%", "Mean Gas Used Per Arbitrage").replace("ymode=log,", "").replace("scatter,", "scatter, only marks,").replace("%colorbartitle%", "Mean Gas Price(Gwei)"))
