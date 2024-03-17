import matplotlib.pyplot as plt
import numpy as np
import csv

labels = []
latency = []

with open('sf/sf.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        instance_type = row["instance type"]
        labels.append(row["sf"])
        latency.append(float(row["average execution time"]))

# Plotting
fig, ax = plt.subplots()

bar_width = 0.2  # Width of the bars

bar_labels = ['red', 'blue', '_red', 'orange']

bar_colors = ['tab:red', 'tab:red', 'tab:blue', 'tab:blue', 'tab:blue', 'tab:orange', 'tab:orange', 'tab:orange']

# Grouped bar positions
bar_positions_sf = np.arange(len(labels[0:3]))
bar_positions_instances = np.arange(len(labels[3:6])) + bar_width
bar_positions_instances_n = np.arange(len(labels[6:9])) + 2 * bar_width

ax.bar(bar_positions_sf, latency[0:3], width=bar_width, label="1769 MB functions (1/10/100 slots)", color='tab:red')
ax.bar(bar_positions_instances, latency[3:6], width=bar_width, label="c6i_large instances (1/5/50 instances)", color='tab:blue')
ax.bar(bar_positions_instances_n, latency[6:9], width=bar_width, label="c6in_large instances (1/5/50 instances)", color='tab:green')

ax.set_xticks((bar_positions_sf + bar_positions_instances + bar_positions_instances_n) / 3)
ax.set_xticklabels(["1", "10", "100"])

ax.legend()
ax.set_xlabel("Scale Factor")
ax.set_ylabel('Latency ms')
ax.set_title('Query Latency Lambda vs. c6i_large')

plt.show()
