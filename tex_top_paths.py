import json
from datetime import datetime
import numpy as np

LINE_TEMPLATE = open('template/data_line.tex').read()
COORDS_CONSTANT = "\\addplot+ coordinates {%coords%};"

def get_moving_average(coords, width):
    coords = np.convolve(coords, np.ones((width,))/width, mode='same')
    return coords

data = json.load(open('data/daily_path_stats.json'))
counts = json.load(open('data/path_counts.json'))
top10 = list(counts.keys())[:10]

ma_bot_profit_graph_lines = ""
for addr in top10:
    bot_profit_coords = ""
    bot_profit = [data[addr][k] for k in data[addr]]
    bot_profit_ma = get_moving_average(bot_profit, 7)
    i = 0
    for k in data[addr].keys():
        bot_profit_coords += "(%s,%f) " % (k, bot_profit_ma[i])
        i += 1
    ma_bot_profit_graph_lines += COORDS_CONSTANT.replace("%coords%", bot_profit_coords) + "\n"

top_bots = []
path2symbol = json.load(open('data/top10_path_symbols.json'))
for p in top10:
    arr = path2symbol[p]
    top_bots.append('-'.join(arr))
open('reports/top10_paths.tex', 'w').write(LINE_TEMPLATE.replace("%plots%", ma_bot_profit_graph_lines).replace("%legendkeys%", ",".join([x for x in top_bots])).replace("%title%", "Top 10 Ring Path Txs, 7-Day Moving Average").replace("%ylabel%", "Number of Txs").replace("%max%", str(2*5000)).replace("%legendpos%", "outer north east").replace("%extraaxisoptions%", ",enlarge x limits=-1,width=.9\\textwidth, height=0.4\\textwidth,x label style={at={(1.15,-.15)},anchor=south,}"))
