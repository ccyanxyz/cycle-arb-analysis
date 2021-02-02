import json

stats = {}
with open('data/cycle_include_router.json') as f:
    for line in f:
        info = json.loads(line)
        path = info['path']
        start = path[0]
        last_start = 0
        i = 1
        while i < len(path):
            if path[i] == start:
                l = (i + 1 - last_start)/2
                '''
                if l == 2:
                    with open('data/len2_tx_hashs.json', 'a') as f:
                        f.write(json.dumps(info['receipt']['transactionHash'])+'\n')
                '''
                if l >= 9:
                    with open('data/long_length_cycle.json', 'a') as f:
                        f.write(json.dumps(info)+'\n')
                if l not in stats.keys():
                    stats[l] = 0
                stats[l] += 1
                if i < len(path) - 1:
                    last_start = i+1
                    i += 1
            i += 1
print(stats)
json.dump(stats, open('data/len_stats_new.json', 'w'))
