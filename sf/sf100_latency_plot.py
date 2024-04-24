import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colormaps
from matplotlib.colors import to_rgba

cmap = plt.get_cmap("Set2")
labels = []
latency = []
df = pd.read_csv("sf/sf.csv")
labels = df["shorthand"]
latency = df["average execution time"]

# Plotting
fig, ax = plt.subplots()
colors = [cmap(0), cmap(0)] + 7 * [cmap(1)] + 7 * [cmap(2)]

ax.bar(labels[0:1], latency[0:1], color = cmap(0), label= "serverless")
ax.bar(labels[1:8], latency[1:8], color = cmap(1), label = "compute instances")
ax.bar(labels[8:15], latency[8:15], color = cmap(2), label = "network instances")

# remove n from ticklabels
tick_labels = [item.get_text()[1:] for item in ax.get_xticklabels()]


print(ax.get_lines())

ax.legend()
ax.set_xticklabels(tick_labels)
ax.set_xlabel("Instance type")
ax.set_ylabel('Latency ms')
ax.set_title('TPC-H SF100, 100 vCPUs')

plt.show()
