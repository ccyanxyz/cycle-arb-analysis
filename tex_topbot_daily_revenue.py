import json
import numpy as np

LINE_TEMPLATE = open('template/data_line.tex').read()
COORDS_CONSTANT = "\\addplot+ coordinates {%coords%};"

def get_moving_average(coords, width):
    coords = np.convolve(coords, np.ones((width,))/width, mode='same')
    return coords

data = json.load(open('data/top10_rev_bot_daily_stats.json'))
total = json.load(open('data/daily_stats.json'))
total_profit = [(total[k]['revenue']-total[k]['cost'])/1e18 for k in total.keys()]
ma_total_profit = get_moving_average(total_profit, 7)

total_profit_coords = ""
i = 0
for k in total.keys():
    total_profit_coords += "(%s,%f) " % (k, ma_total_profit[i])
    i += 1

ma_bot_profit_graph_lines = COORDS_CONSTANT.replace("addplot+", "addplot+[black]").replace("%coords%", total_profit_coords) + "\n"
for addr in data.keys():
    bot_profit_coords = ""
    bot_profit = [data[addr][k]['profit']/1e18 for k in data[addr]]
    bot_profit_ma = get_moving_average(bot_profit, 7)
    i = 0
    for k in data[addr].keys():
        bot_profit_coords += "(%s,%f) " % (k, bot_profit_ma[i])
        i += 1
    ma_bot_profit_graph_lines += COORDS_CONSTANT.replace("%coords%", bot_profit_coords) + "\n"

top_bots = list(data.keys())

open('reports/topbot_daily_revenue.tex', 'w').write(LINE_TEMPLATE.replace("%plots%", ma_bot_profit_graph_lines).replace("%legendkeys%", "Market Total," + ",".join([x[:8] + ".." for x in top_bots])).replace("%title%", "Ring Arbitrage Profit Per Bot, 7-Day Moving Average").replace("%ylabel%", "Daily Arbitrage Profit (ETH)").replace("%max%", str(2*max(ma_total_profit))).replace("%legendpos%", "outer north east").replace("%extraaxisoptions%", ",enlarge x limits=-1,width=.9\\textwidth, height=0.4\\textwidth,x label style={at={(1.15,-.15)},anchor=south,}"))
