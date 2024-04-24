import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colormaps
from matplotlib.colors import to_rgba
import matplotlib.patches as mpatches
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

cmap = plt.get_cmap("Set2")
labels = []
cost = []
df = pd.read_csv("sf/sf.csv")
df["on demand"] = 0
df["spot"] = 0
labels = df["shorthand"]

df2 = pd.read_csv("prices.csv")
for i in range(0, len(df["spot"])):
    for j in range(0, len(df2["instance type"])):
        if df["instance type"][i] == df2["instance type"][j]:
            df["on demand"][i] = df2["on demand"][j]
            df["spot"][i] = df2["spot"][j]



clustered_labels = [labels[0] , "svlz"]
for l1, l2 in zip(labels[1:6], labels[8:13]):
    clustered_labels.append(l1)
    clustered_labels.append(l2)
    clustered_labels.append(l2+"z")


cost_on_demand = df["average execution time"] / 1000 * df["instances running"] * df["on demand"] / 3600
cost_spot = df["average execution time"] / 1000 * df["instances running"] * df["spot"] / 3600
#cost = df["cost per query"] #on demand
serverless_cost = df["cost per query"][0]

clustered_costs_demand = [serverless_cost,0]
for l1, l2 in zip(cost_on_demand[1:6], cost_on_demand[8:13]):
    clustered_costs_demand.append(l1)
    clustered_costs_demand.append(l2)
    clustered_costs_demand.append(0)

clustered_costs_spot = [serverless_cost,0]
for l1, l2 in zip(cost_spot[1:6], cost_spot[8:13]):
    clustered_costs_spot.append(l1)
    clustered_costs_spot.append(l2)
    clustered_costs_spot.append(0)

#bottomize on demand

bottomized_on_demand = []
for c1, c2 in zip(clustered_costs_demand, clustered_costs_spot):
    bottomized_on_demand.append(c1-c2)
# ignore serverless
clustered_costs_spot[0] = 0
bottomized_on_demand[0] = clustered_costs_demand[0]



print("bottom: ", bottomized_on_demand)


# Plotting
fig, ax = plt.subplots()
cols = [cmap(0)] + 10 * [cmap(1), cmap(2)]
ax.bar(clustered_labels, clustered_costs_spot, hatch = "///", color = cols)
ax.bar(clustered_labels, bottomized_on_demand, bottom = clustered_costs_spot, color = cols)

print(ax.get_lines())
# we build the legend by hand
svl_patch = mpatches.Patch(color = cmap(0), label = "serverless")
compute_patch = mpatches.Patch(color = cmap(1), label = "compute-optimized")
network_patch = mpatches.Patch(color = cmap(2), label = "networked-optimized")
spot_patch = mpatches.Patch(facecolor="None", edgecolor="black", hatch="///", label = "spot cost")

tick_labels = ["SVL", "", "L", "", "XL", "", "2XL", "", "4XL", "", "8XL"]
ax.set_xticks([0, 2.5, 2.5, 5.5, 5.5, 8.5, 8.5, 11.5, 11.5, 14.5, 14.5])
ax.set_xticklabels(tick_labels)

ax.legend(loc = "lower left", handles = [svl_patch, compute_patch, network_patch, spot_patch], bbox_to_anchor=(1.0, 0.0))
#ax.set_xticklabels(tick_labels)
ax.set_xlabel("Virtual server size")
ax.set_ylabel('Cost USD')
ax.set_ylim(0,0.0045)
#ax.set_title('TPC-H SF100, 100 vCPUs')
fig.set_figheight(3)
fig.set_figwidth(6)
fig.tight_layout()
plt.savefig('tpch_cost.png', dpi=300)
plt.show()
