import json

t = 1593360000
ts = json.load(open('data/ts.json'))
count = 0
total = 0
with open('data/cycle_include_router.json') as f:
    for line in f:
        info = json.loads(line)
        bn = int(info['receipt']['blockNumber'], 16)
        total += 1
        if ts[str(bn)] > t:
            break
        if info['revenue'] <= 0:
            count += 1
            with open('data/neg_revenue_txs_before_1593360000.json', 'a') as f1:
                f1.write(json.dumps(info)+'\n')
print(total, count)
