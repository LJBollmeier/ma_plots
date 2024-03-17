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
instance_cost = df["instance cost"]
instance_cost_per_minute = df["instances running"] * df["spot"] / 60
print(instance_cost_per_minute)
request_cost = df["request cost"]
all_costs = [worker_cost, coordinator_cost, instance_cost, request_cost]
bottom = np.zeros(len(worker_cost))
labels = ["0", "1", "2", "3"]

queries_per_minute = range(1,31)

fig, ax = plt.subplots()
for i in range(0,4):
    costs = [(instance_cost_per_minute[i] + q * coordinator_cost[i] / repetitions[i] + worker_cost[i] * q / repetitions[i] + request_cost[i] * q / repetitions[i]) / q for q in queries_per_minute]
    print(costs[0])
    ax.plot(queries_per_minute, costs, color = cmap(i), label=labels[i])
# remove n from ticklabels
#tick_labels = [item.get_text()[1:] for item in ax.get_xticklabels()]

print(ax.get_lines())

ax.legend(loc = "lower right")
#ax.legend(loc='upper left', bbox_to_anchor=(1, 0.5))

#ax.set_xticklabels(tick_labels)
ax.set_xlabel("Queries per minute")
ax.set_ylabel('Execution Time (ms)')
#ax.set_title('TPC-H SF10')
fig.set_figheight(3)
fig.set_figwidth(5)
fig.tight_layout()
plt.savefig('he_tpch_cost_once', dpi=300)
#plt.show()


fig, ax = plt.subplots()
labels = ["serverless", "1 instance", "2 instances", "3 instances"]
for i in range(0,4):
    max_queries_per_minute = 60000/df["average execution time"][i]
    if i == 0:
        max_queries_per_minute = 50
    queries_per_minute = range(5,int(max_queries_per_minute)+1)
    
    costs = [(instance_cost_per_minute[i] + q * coordinator_cost[i] / repetitions[i] + worker_cost[i] * q / repetitions[i] + request_cost[i] * q / repetitions[i]) / q for q in queries_per_minute]
    extrapolated_costs = [(instance_cost_per_minute[i] + q * coordinator_cost[i] / repetitions[i] + worker_cost[i] * int(max_queries_per_minute) / repetitions[i] + worker_cost[0] * (q-int(max_queries_per_minute)) / repetitions[i]  + request_cost[i] * q / repetitions[i]) / q for q in range(int(max_queries_per_minute) + 1, 51)]
    print(extrapolated_costs)
    costs += extrapolated_costs
    
    ax.plot(range(5,51), costs, color = cmap(i), label=labels[i])
# remove n from ticklabels
#tick_labels = [item.get_text()[1:] for item in ax.get_xticklabels()]

print(ax.get_lines())

ax.legend(loc = "lower left", bbox_to_anchor=(1.0,0.0))
#ax.legend(loc='upper left', bbox_to_anchor=(1, 0.5))

#ax.set_xticklabels(tick_labels)
ax.set_xlabel("Queries per minute")
ax.set_ylabel('Cost per Query (USD)')
#ax.set_title('TPC-H SF10')
fig.set_figheight(3)
fig.set_figwidth(5)
fig.tight_layout()
plt.savefig('he_tpch_cost_once', dpi=300)
plt.show()