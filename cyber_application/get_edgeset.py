

import pandas as pd
import gzip

path = 'cyber_application/data/'

file = 'auth_weekly_filtered.gz'


nodes = pd.read_csv(path + 'nodes_subnetwork.csv')
nodes = nodes['0'].values.tolist()

source_counts = dict()

with gzip.open(path + file, 'r') as fin:
    for line in fin:
        line = line.decode("utf-8").strip().split(',')
        if line[8] == 'Success' and line[7] == 'LogOn' and line[6] == 'Network' and line[1] in nodes:
            if str(line[1]) in source_counts.keys():
                source_counts[str(line[1])].add((str(line[3]), int(int(line[0])/24)))
            else:
                source_counts[str(line[1])] = set()
                source_counts[str(line[1])].add((str(line[3]), int(int(line[0])/24)))

        print('time_' + str(line[0]))


E_d = []

for i in range(len(nodes)):
    s_i_d = set([s for s in source_counts[nodes[i]]])
    for j in range(i+1, len(nodes)):
        s_j_d = set([s for s in source_counts[nodes[j]]])
        if len(s_i_d.intersection(s_j_d)) > 0:
            E_d += [[nodes[i], nodes[j]]]
    print(i)


E_d = pd.DataFrame(E_d)
E_d.to_csv(path+'edgeset_subnetwork.csv', index=False)

