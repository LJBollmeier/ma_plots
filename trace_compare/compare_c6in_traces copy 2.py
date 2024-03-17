import pandas as pd
import matplotlib.pyplot as plot
import os
import regex as re
import sys

base_dir = "trace_compare/c6i_sf1_instances1_repetitions10000/"
instances = os.listdir(base_dir)
instances = instances[0:1]
network_traces = [base_dir + instance + "/network_trace" for instance in instances]
cpu_traces = [base_dir + instance + "/cpu_trace" for instance in instances]
worker_dirs = [base_dir + instance + "/worker/" for instance in instances]
colors = ["red", "blue"]
fig,ax = plot.subplots(len(cpu_traces) * 3)

instance_start = sys.float_info.max
for instance in instances:
    n_instance = base_dir + instance
    fd = open(n_instance + "/logger")
    fd.readline()
    fd.readline()
    start = int(fd.readline().split(",")[0]) * 1000000
    instance_start = min(start, instance_start)


def parse_logs(path):
    starts = []
    finishes = []
    operators = []

    fd = open(path)
    lc = 0
    for line in fd:
        lc += 1
        re_expression = "([0-9]+),operator started: (.+)"
        matches = re.findall(re_expression, line)
        if len(matches) > 0:
            starts.append(int(matches[0][0])*1000000)
        re_expression = "([0-9]+),operator finished: (.+)"
        matches = re.findall(re_expression, line)
        if len(matches) > 0:
            finishes.append(int(matches[0][0]) * 1000000)
            operators.append(matches[0][1])
            if (finishes[-1] - starts[-1] > 5000000000):
                print(path, lc, (starts[-1]-instance_start) / 1000000000 , (finishes[-1]-instance_start) /1000000000)
    fd.close()
        
    return starts, finishes, operators        

plot_index = 0
xmin = 0
xmax = 20

operator_colors = {"Import" : "blue", "Export" : "red", "FilterOperator" : "orange", "AggregateHash" : "green", "Projection" : "brown", "Alias" : "black"}

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
    ax[plot_index].plot(df["Time"], df["BytesReceived"] / 1000000  * 10, color = "red")
    ax[plot_index].set_xlabel("Time (s)")
    ax[plot_index].set_ylabel("Network bandwidth (MB/s)")
    ax[plot_index].set_title("C6i_large network bandwidth over time")
    ax[plot_index].set_xlim(xmin,xmax)
    plot_index += 1

    registered_labels = {}
    for file in os.listdir(worker_dir):
        full_path = os.path.join(worker_dir, file)
        starts, finishes, operators = parse_logs(full_path)
        starts = [(time - instance_start) / 1000000000 for time in starts]
        finishes = [(time - instance_start) / 1000000000 for time in finishes]
        for start, finish, operator in zip(starts, finishes, operators):
            t = [start, start, finish, finish]
            o = [0,1,1,0]
            if operator not in registered_labels.keys():
                ax[plot_index].plot(t, o, label=operator, color= operator_colors[operator])
                registered_labels[operator] = operator
            else:
                ax[plot_index].plot(t, o, color= operator_colors[operator])


        ax[plot_index].set_xlim(xmin,xmax)
        ax[plot_index].legend()

    plot_index += 1
#plot.plot(df["Time"], df["BytesReceived"], color = color)
#plot.plot(df["Time"], df["BytesSend"], color = color)

plot.show()
    
    