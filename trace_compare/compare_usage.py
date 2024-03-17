import pandas as pd
import matplotlib.pyplot as plot
import os
import regex as re
import sys

base_dir = "trace_compare/c6i_32xlarge_sf100_instances1_repetitions10/"
#base_dir = "trace_compare/c6i_large_sf100_instances50_repetitions10/"
instances = os.listdir(base_dir)
instances = instances[0:5]
network_traces = [base_dir + instance + "/network_trace" for instance in instances]
cpu_traces = [base_dir + instance + "/cpu_trace" for instance in instances]
worker_dirs = [base_dir + instance + "/worker/" for instance in instances]
colors = ["red", "blue"]
fig,ax = plot.subplots(len(cpu_traces) * 2)
print(cpu_traces)

instance_start = sys.float_info.max
plot_index = 0
xmin = 0
xmax = 20
for network_trace in network_traces:
    with open(network_trace) as fd:
        df = pd.read_csv(fd)
    instance_start = min(df["Time"][0], instance_start)

for nt, ct, worker_dir in zip(network_traces, cpu_traces, worker_dirs):
    with open(ct) as fd:
        df = pd.read_csv(fd)

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

    with open(nt) as fd:
        df = pd.read_csv(fd)
    df["Time"] = (df["Time"] - instance_start) / 1000000000
    ax[plot_index].plot(df["Time"], df["BytesReceived"] / 1000000  * 20, color = "red")
    ax[plot_index].set_xlabel("Time (s)")
    ax[plot_index].set_ylabel("Network bandwidth (MB/s)")
    ax[plot_index].set_title("C6i_large network bandwidth over time")
    ax[plot_index].set_xlim(xmin,xmax)
    plot_index += 1

#plot.plot(df["Time"], df["BytesReceived"], color = color)
#plot.plot(df["Time"], df["BytesSend"], color = color)

plot.show()
    
    