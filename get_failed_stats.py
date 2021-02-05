import json
import os

addr_stats = json.load(open('data/addr_stats_with_sigs.json'))
stats = {}
idx = 0
for addr in os.listdir('/data/tx_info'):
    print(idx, addr)
    if addr == '0x7a250d5630b4cf539739df2c5dacb4c659f2488d':
        continue
    if addr not in stats:
        stats[addr] = { 'fail_count': 0, 'fail_cost': 0, 'total_txs': 0, 'total_cost': 0 }
    with open('/data/tx_info/'+addr) as f:
        for line in f:
            info = json.loads(line)
            stats[addr]['total_txs'] += 1
            stats[addr]['total_cost'] += int(info['gasPrice']) * int(info['gasUsed'])
            if not info['to'] or info['to'] == "":
                continue
            func_sig = info['input'][:10]
            if info['txreceipt_status'] == "0" and func_sig in addr_stats[addr.lower()]['sigs']:
                stats[addr]['fail_count'] += 1
                stats[addr]['fail_cost'] += int(info['gasPrice']) * int(info['gasUsed'])
    idx += 1
json.dump(stats, open('data/arb_fail_stats_no_router.json', 'w'))
