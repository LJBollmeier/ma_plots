import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colormaps
from matplotlib.colors import to_rgba
import matplotlib.patches as mpatches

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


cost_on_demand = df["average execution time"] / 1000 * df["instances running"] * df["on demand"] / 3600
cost_spot = df["average execution time"] / 1000 * df["instances running"] * df["spot"] / 3600
#cost = df["cost per query"] #on demand
serverless_cost = df["cost per query"][0]

# Plotting
fig, ax = plt.subplots()
colors = [cmap(0)] + 7 * [cmap(1)] + 7 * [cmap(2)]

ax.bar(labels[0:1], serverless_cost, color = cmap(0), label= "serverless")
ax.bar(labels[1:6], cost_spot[1:6], color = cmap(3), hatch = "///", label = "compute instances")
ax.bar(labels[1:6], cost_on_demand[1:6]-cost_spot[1:6], bottom = cost_spot[1:6], color = cmap(3), label = "compute instances")

ax.bar(labels[8:13], cost_spot[8:13], color = cmap(2), hatch = "///",  label = "network instances")
ax.bar(labels[8:13], cost_on_demand[8:13]-cost_spot[8:13], bottom = cost_spot[8:13],  color = cmap(2), label = "network instances")

# remove n from ticklabels
tick_labels = [item.get_text()[1:] for item in ax.get_xticklabels()]


print(ax.get_lines())
# we build the legend by hand
svl_patch = mpatches.Patch(color = cmap(0), label = "serverless")
compute_patch = mpatches.Patch(color = cmap(3), label = "compute instances")
network_patch = mpatches.Patch(color = cmap(2), label = "network instances")
spot_patch = mpatches.Patch(facecolor="None", edgecolor="black", hatch="///", label = "spot cost")



ax.legend(loc = "lower left", handles = [svl_patch, compute_patch, network_patch, spot_patch], bbox_to_anchor=(1.0, 0.0))
ax.set_xticklabels(tick_labels)
ax.set_xlabel("Instance type")
ax.set_ylabel('Cost USD')
ax.set_title('TPC-H SF100, 100 vCPUs')
fig.set_figheight(3)
fig.set_figwidth(6)
fig.tight_layout()
plt.savefig('tpch_cost.png', dpi=300)
plt.show()
