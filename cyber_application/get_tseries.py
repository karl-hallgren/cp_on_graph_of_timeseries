
import pandas as pd
import gzip
from collections import Counter


path = 'cyber_application/data/'

file = 'auth_weekly_filtered.gz'


nodes = pd.read_csv(path+'nodes_subnetwork.csv')
nodes = nodes['0'].values.tolist()


source_counts_net = {v: Counter() for v in nodes}

i = 0


with gzip.open(path + file, 'r') as fin:
    for line in fin:
        line = line.decode("utf-8").strip().split(',')
        hour = int(line[0])
        user = str(line[1])
        source = str(line[3])
        #dest = str(line[4])
        #authtype = str(line[5])
        logtype = str(line[6])
        authorien = str(line[7])
        #success = str(line[8])
        count = int(line[9])

        if user in nodes:
            if logtype == 'Network' and authorien == 'LogOn':
                source_counts_net[user][(source, hour)] += count

        print('time_' + str(line[0]))
        i += 1


times = list(range(58*24))

for v in nodes:
    source_v = list(set([key[0] for key in source_counts_net[v].keys()]))
    out_v = [[source_counts_net[v][(s, t)] for s in source_v] for t in times]
    out_v = pd.DataFrame(out_v)
    out_v.columns = source_v
    out_v.to_csv(path + 'tseries/x_' + str(v) + '.csv', index=False)



