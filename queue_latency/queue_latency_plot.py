import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
cmap = plt.get_cmap("Set2")
import pandas as pd
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

df = pd.read_csv("queue_latency/data/latencies.csv", delimiter=",")
latencies = df["average_latency"].tolist()
perc_latencies = df["90th_perc"]

queue_size = [str(x) for x in df["queue_size"].tolist()]
queue_size[-1] = "unlimited"
f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.bar(queue_size,latencies, color = cmap(0))
ax1.bar(queue_size, perc_latencies-latencies, bottom = latencies, color = cmap(1))
ax2.bar(queue_size,latencies, color = cmap(0))
ax2.bar(queue_size, perc_latencies-latencies, bottom = latencies, color = cmap(1))

ax1.set_ylim(130000,250000)
ax2.set_ylim(0,20000)
ax1.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.xaxis.tick_top()
ax1.tick_params(labeltop=False)  # don't put tick labels at the top
ax2.xaxis.tick_bottom()

d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
ax1.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal


mean_patch = mpatches.Patch(color = cmap(0), label = "average")
perc_patch = mpatches.Patch(color = cmap(1), label = "90th percentile")
ax1.legend(loc = "upper left", handles = [mean_patch, perc_patch])
f.supylabel("Execution latency (ms)")
f.supxlabel("Size of ready queue")
f.tight_layout()
f.set_figwidth(6)
f.set_figheight(3)
f.savefig("queue_latency", dpi = 300)
plt.show()