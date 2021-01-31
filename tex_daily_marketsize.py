import json
import numpy as np

tex = open('template/breadth.tex').read()
data = json.load(open('data/daily_stats.json'))

def get_cum_rev(arr):
    l = []
    for i in range(len(arr)):
        l.append(sum(arr[:i]))
    return l

revenue = [data[k]['revenue']/1e18 for k in data.keys()]
cost = [data[k]['cost']/1e18 for k in data.keys()]
count = [data[k]['count'] for k in data.keys()]
profit = [(data[k]['revenue']-data[k]['cost'])/1e18 for k in data.keys()]
cumu = get_cum_rev(revenue)

date = list(data.keys())

def get_moving_average(coords, width):
    coords = np.convolve(coords, np.ones((width,))/width, mode='same')
    return coords

eth_revenue_coords = ""
for d in data.keys():
    eth_revenue_coords += "(%s,%f) [%f]" % (d, data[d]['revenue']/1e18, data[d]['count'])

ma_revenue = get_moving_average(revenue, 7)
ma_eth_coords = ""
cum_eth_coords = ""
for i in range(len(date)):
    ma_eth_coords += "(%s,%f) " % (date[i], ma_revenue[i])
    cum_eth_coords += "(%s,%f) " % (date[i], cumu[i]) 

open('reports/daily_revenue.tex', 'w').write(
        tex.replace("%coords%", eth_revenue_coords).replace("%macoords%", ma_eth_coords).replace("%title%", "Ring Arbitrage Market Size (ETH)").replace("%ylabel%", "Daily Revenue (ETH)").replace("%cumcoords%", cum_eth_coords).replace("%extra%", "").replace("%max%", str(2*max(cumu))).replace("%colorbartitle%", "\\# Txs").replace("%extraaxisoptions%", " point meta max=1000,").replace("%extracolorbar%", "ytick={0,1000,2000,...,3000}, extra y ticks={4000}, extra y tick labels={4000+}"))
