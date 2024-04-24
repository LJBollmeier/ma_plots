import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.patches as mpatches
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

cmap = plt.get_cmap("Set2")
labels = []
latency = []
df = pd.read_csv("sf/sf.csv")
labels = df["shorthand"]
latency = df["average execution time"]

# Plotting
fig, ax = plt.subplots()
cols = [cmap(0), cmap(0)] + 10 * [cmap(1), cmap(2)]

clustered_latencies = [latency[0], 0]
for l1, l2 in zip(latency[1:6], latency[8:13]):
    clustered_latencies.append(l1)
    clustered_latencies.append(l2)
    clustered_latencies.append(0)

clustered_labels = [labels[0] , "svlz"]
for l1, l2 in zip(labels[1:6], labels[8:13]):
    clustered_labels.append(l1)
    clustered_labels.append(l2)
    clustered_labels.append(l2+"z")

ax.bar(clustered_labels, clustered_latencies, color= cols)

# ax.bar(labels[0:1], latency[0:1], color = cmap(0), label= "serverless")
# ax.bar(labels[1:6], latency[1:6], color = cmap(1), label = "compute instances")
# ax.bar(labels[8:13], latency[8:13], color = cmap(2), label = "network instances")

# remove n from ticklabels
#tick_labels = [item.get_text()[1:] for item in ax.get_xticklabels()]
tick_labels = ["SVL", "", "L", "", "XL", "", "2XL", "", "4XL", "", "8XL"]

print(ax.get_lines())

ax.legend(loc="lower right")
ax.set_xticks([0, 2.5, 2.5, 5.5, 5.5, 8.5, 8.5, 11.5, 11.5, 14.5, 14.5])
ax.set_xticklabels(tick_labels)
ax.set_xlabel("Virtual server size")
ax.set_ylabel('Latency ms')

svl_patch = mpatches.Patch(color = cmap(0), label = "serverless")
compute_patch = mpatches.Patch(color = cmap(1), label = "compute-optimized")
network_patch = mpatches.Patch(color = cmap(2), label = "network-optimized")
ax.legend(loc = "upper left", handles = [svl_patch, compute_patch, network_patch], bbox_to_anchor=(1, 1))
#ax.set_title('TPC-H SF100, 100 vCPUs')
fig.set_figheight(3)
fig.set_figwidth(6)
fig.tight_layout()
plt.savefig('tpch_latency.png', dpi=300)

plt.show()
