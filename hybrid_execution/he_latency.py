import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colormaps
from matplotlib.colors import to_rgba
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

cmap = plt.get_cmap("Set2")
labels = []
latency = []
df = pd.read_csv("hybrid_execution/he.csv")
labels = df["shorthand"]
latency = df["average execution time"]

# Plotting
fig, ax = plt.subplots()

ax.bar(labels[0:1], latency[0:1], color = cmap(0), label= "serverless execution")
ax.bar(labels[1:3], latency[1:3], color = cmap(1), label = "hybrid execution")
ax.bar(labels[3:4], latency[3:4], color = cmap(2), label = "virtual server execution")

# remove n from ticklabels
#tick_labels = [item.get_text()[1:] for item in ax.get_xticklabels()]


print(ax.get_lines())

ax.legend(loc = "upper left", bbox_to_anchor=(1.0, 1.0))
#ax.set_xticklabels(tick_labels)
ax.set_xlabel("Virtual server count")
ax.set_ylabel('Execution time (ms)')
#ax.set_title('TPC-H SF10')
fig.set_figheight(3)
fig.set_figwidth(6)
fig.tight_layout()
plt.savefig('he_tpch_latency', dpi=300)
plt.show()
