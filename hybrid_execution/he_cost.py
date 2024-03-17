import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colormaps
from matplotlib.colors import to_rgba

cmap = plt.get_cmap("Set2")
latency = []
df = pd.read_csv("hybrid_execution/he.csv")
repetitions = df["repetitions"]

df2 = pd.read_csv("prices.csv")
df["spot"] = 0
df["on demand"] = 0
for i in range(0, len(df["spot"])):
    for j in range(0, len(df2["instance type"])):
        if df["instance type"][i] == df2["instance type"][j]:
            df["on demand"][i] = df2["on demand"][j]
            df["spot"][i] = df2["spot"][j]


cost_on_demand = df["average execution time"] / 1000 * df["instances running"] * df["on demand"] / 3600
cost_on_demand *= repetitions
cost_spot = df["average execution time"] / 1000 * df["instances running"] * df["spot"] / 3600
cost_spot *= repetitions

instances = df["shorthand"]
worker_cost = df["worker function cost"]
coordinator_cost = df["coordinator function cost"]
instance_cost = cost_spot #df["instance cost"]
request_cost = df["request cost"]
bottom = np.zeros(len(worker_cost))
all_costs = [request_cost, coordinator_cost, worker_cost, cost_spot]
labels = ["request", "coordinator", "serverless", "instance"]

fig, ax = plt.subplots()
for cost,i in zip(all_costs, range(0, len(all_costs))):
    cost = cost / repetitions
    ax.bar(instances, cost, bottom=bottom, color = cmap(i), label=labels[i])

    bottom += cost
# remove n from ticklabels
#tick_labels = [item.get_text()[1:] for item in ax.get_xticklabels()]


print(ax.get_lines())

#ax.legend(loc = "lower right")
ax.legend(loc='upper left', bbox_to_anchor=(1, 0.5))
#ax.set_xticklabels(tick_labels)
ax.set_xlabel("Instance count")
ax.set_ylabel('Cost per Query (USD)')
ax.set_ylim(0,0.00055)
#ax.set_title('TPC-H SF10')
fig.set_figheight(3)
fig.set_figwidth(5)
fig.tight_layout()
plt.savefig('he_tpch_cost', dpi=300)
plt.show()
