import pandas as pd
import matplotlib.pyplot as plot

network_traces_to_compare = ["trace_compare/c6i_sf10_repetitions10/i-0a8fce90941240166/network_trace", "trace_compare/c6in_sf10_repetitions10/i-0d522ea34defac8d7/network_trace"]

cpu_traces = ["trace_compare/c6i_sf10_repetitions10/i-0a8fce90941240166/cpu_trace", "trace_compare/c6in_sf10_repetitions10/i-0d522ea34defac8d7/cpu_trace"]
colors = ["red", "blue"]
fig,ax = plot.subplots(4)

traces = cpu_traces
fn = cpu_traces[0]
with open(fn) as fd:
    df = pd.read_csv(fd)
df["Time"] = (df["Time"] - df["Time"][0]) / 1000000000
ax[0].plot(df["Time"], df["User"] + df["Kernel"], color = "red")
ax[0].set_xlabel("Time (s)")
ax[0].set_ylabel("CPU Usage")
ax[0].set_title("C6i_large cpu usage over time")
#plot.plot(df["Time"], df["BytesReceived"], color = color)
#plot.plot(df["Time"], df["BytesSend"], color = color)

fn = network_traces_to_compare[0]
traces = network_traces_to_compare
with open(fn) as fd:
    df = pd.read_csv(fd)
df["Time"] = (df["Time"] - df["Time"][0]) / 1000000000
ax[1].plot(df["Time"], df["BytesReceived"] / 1000000  * 10, color = "red")
ax[1].set_xlabel("Time (s)")
ax[1].set_ylabel("Network bandwidth (MB/s)")
ax[1].set_title("C6i_large network bandwidth over time")

#ax[1].plot(df["Time"], df["BytesSend"], color = "blue")

traces = cpu_traces
fn = cpu_traces[1]
with open(fn) as fd:
    df = pd.read_csv(fd)
df["Time"] = (df["Time"] - df["Time"][0]) / 1000000000
ax[2].plot(df["Time"], df["User"] + df["Kernel"], color = "red")
ax[2].set_xlabel("Time (s)")
ax[2].set_ylabel("CPU Usage")
ax[2].set_title("C6in_large cpu usage over time")
#plot.plot(df["Time"], df["BytesReceived"], color = color)
#plot.plot(df["Time"], df["BytesSend"], color = color)

fn = network_traces_to_compare[1]
traces = network_traces_to_compare
with open(fn) as fd:
    df = pd.read_csv(fd)
df["Time"] = (df["Time"] - df["Time"][0]) / 1000000000
ax[3].plot(df["Time"], df["BytesReceived"] / 1000000  * 10, color = "red")
ax[3].set_xlabel("Time (s)")
ax[3].set_ylabel("Network bandwidth (MB/s)")
ax[3].set_title("C6in_large network bandwidth over time")
#ax[3].plot(df["Time"], df["BytesSend"], color = "blue")
plot.show()
    
    