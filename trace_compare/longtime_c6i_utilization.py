import pandas as pd
import matplotlib.pyplot as plot
import os
import regex as re
import sys

base_dir = "trace_compare/c6i_sf1_instances1_repetitions1000/"
instances = os.listdir(base_dir)
instances = instances[0:1]
network_traces = [base_dir + instance + "/network_trace" for instance in instances]
cpu_traces = [base_dir + instance + "/cpu_trace" for instance in instances]
worker_dirs = [base_dir + instance + "/worker/" for instance in instances]
colors = ["red", "blue"]
fig,ax = plot.subplots(len(cpu_traces) * 3)


plot_index = 0
xmin = 0
xmax = 1200


operator_colors = {"Import" : "blue", "Export" : "red", "FilterOperator" : "orange", "AggregateHash" : "green", "Projection" : "brown", "Alias" : "black"}

with open(cpu_traces[0]) as fd:
    df = pd.read_csv(fd)
instance_start = df["Time"][0]
df["Time"] = (df["Time"] - instance_start) / 1000000000
ax[plot_index].plot(df["Time"], df["User"] + df["Kernel"], color = "red", label= "All")
ax[plot_index].plot(df["Time"], df["User"], color = "blue", label="User")
ax[plot_index].plot(df["Time"], df["Kernel"], color = "green", label="Kernel")

ax[plot_index].set_xlabel("Time (s)")
ax[plot_index].set_ylabel("CPU Usage")
ax[plot_index].set_title("C6i_large cpu usage over time")
ax[plot_index].set_xlim(xmin,xmax)
ax[plot_index].legend()
plot_index += 1




with open(network_traces[0]) as fd:
    df = pd.read_csv(fd)

bytes_avg = df["BytesReceived"].sum() / 10 / 7
print(bytes_avg)
df["Time"] = (df["Time"] - instance_start) / 1000000000
ax[plot_index].plot(df["Time"], df["BytesReceived"] / 1000000  * 10, color = "red")
ax[plot_index].set_xlabel("Time (s)")
ax[plot_index].set_ylabel("Network bandwidth (MB/s)")
ax[plot_index].set_title("C6i_large network bandwidth over time")
ax[plot_index].set_xlim(xmin,xmax)
plot_index += 1

# df["BytesReceived"] = df["BytesReceived"].rolling(window = 10).mean()*20
# ax[plot_index].plot(df["Time"], df["BytesReceived"], color = "orange")
# ax[plot_index].set_xlabel("Time (s)")
# ax[plot_index].set_ylabel("Network bandwidth (MB/s)")
# ax[plot_index].set_title("C6i_large network bandwidth over time windowed")
# ax[plot_index].set_xlim(xmin,xmax)


#plot.plot(df["Time"], df["BytesReceived"], color = color)
#plot.plot(df["Time"], df["BytesSend"], color = color)

plot.show()
    
    