import matplotlib.pyplot as plot
cmap = plot.get_cmap("Set2")
import pandas as pd
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

df = pd.read_csv("server_slots/server_slots.csv")
parallel_queries = df["parallel queries"]
average_execution_time = df["average execution time"]
fig,ax = plot.subplots(1,2)
fig.set_figwidth(6)
fig.set_figheight(3)
ax[0].plot(parallel_queries, average_execution_time, color = cmap(0))
ax[0].set_ylabel("Average query latency (ms)")
ax[0].set_xlabel("Number of parallel queries")
ax[0].set_ylim(0,7000)

print(average_execution_time[1] / average_execution_time[0])
print(1000 / average_execution_time[0] / 1.5)
print(2*1000/average_execution_time[1]/1.5)
print(8*1000/average_execution_time[7]/1.5)
print(average_execution_time[7] / average_execution_time[0])

ax[1].plot(parallel_queries, 1000 / (average_execution_time / parallel_queries), color = cmap(0))
ax[1].set_ylabel("Throughput (fragments/s)")
ax[1].set_xlabel("Number of parallel queries")
ax[1].set_ylim(0,1.7)
#ax[0].tight_layout()
plot.tight_layout()
plot.savefig("latency_per_slot", dpi = 300)
plot.show()
             
