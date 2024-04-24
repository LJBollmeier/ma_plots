import pandas as pd
import matplotlib.pyplot as plot
import os
import regex as re
import sys
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

base_dirs = ["trace_compare/c6i_large_sf100_instances50_repetitions10/", "trace_compare/c6in_large_sf100_instances50_repetitions10/"]
instances = [os.listdir(dir)[0] for dir in base_dirs]
instances = instances[0:1]
print (instances)
network_traces = [base_dir + instance + "/network_trace" for base_dir, instance in zip(base_dirs, instances)]
cpu_traces = [base_dir  + instance + "/cpu_trace" for base_dir, instance in zip(base_dirs, instances)]
worker_dirs = [base_dir + instance + "/worker/" for base_dir, instance in zip(base_dirs, instances)]
colors = ["red", "blue"]
fig,ax = plot.subplots(len(instances) * 2)

instance_starts = []
for base_dir, instance in zip(base_dirs, instances):
    n_instance = base_dir + instance
    fd = open(n_instance + "/logger")
    fd.readline()
    fd.readline()
    start = int(fd.readline().split(",")[0])
    instance_starts.append(start)
print(instance_starts)


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
            starts.append(int(matches[0][0]))
        re_expression = "([0-9]+),operator finished: (.+)"
        matches = re.findall(re_expression, line)
        if len(matches) > 0:
            finishes.append(int(matches[0][0]))
            operators.append(matches[0][1])
            if (finishes[-1] - starts[-1] > 5000000000):
                print(path, lc, (starts[-1]-instance_start) / 1000000000 , (finishes[-1]-instance_start) /1000000000)
    fd.close()
        
    return starts, finishes, operators        

plot_index = 0
xmins = [10.2,12]
xmaxs = [11.68,5]

operator_colors = {"Import" : "blue", "Export" : "red", "FilterOperator" : "orange", "AggregateHash" : "green", "Projection" : "brown", "Alias" : "black"}

cmap = plot.get_cmap("Set2")

for nt, ct, worker_dir, instance_start, xmin, xmax in zip(network_traces, cpu_traces, worker_dirs, instance_starts, xmins, xmaxs):
    with open(ct) as fd:
        df = pd.read_csv(fd)
    print(instance_starts)
    df["Time"] = (df["Time"] / 1000000 - instance_start) / 1000 -xmin
    ax[plot_index].plot(df["Time"], df["User"] + df["Kernel"], color = cmap(0), label= "All")
    ax[plot_index].plot(df["Time"], df["User"], color = cmap(1), label="User")
    ax[plot_index].plot(df["Time"], df["Kernel"], color = cmap(2), label="Kernel")
    
    ax[plot_index].set_xlabel("Time (s)")
    ax[plot_index].set_ylabel("CPU usage")
    #ax[plot_index].set_title("c6i_large cpu usage")
    ax[plot_index].set_xlim(0,xmax-xmin)
    ax[plot_index].legend(loc = "upper right", bbox_to_anchor=(0.2,1.6))
    plot_index += 1

    with open(nt) as fd:
        df = pd.read_csv(fd)
    df["Time"] = (df["Time"] / 1000000 - instance_start) / 1000 - xmin
    ax[plot_index].plot(df["Time"], (df["BytesReceived"] + df["BytesSend"]) / 1000000  * 50, color = cmap(3))
    ax[plot_index].set_xlabel("Time (s)")
    ax[plot_index].set_ylabel("Network bandwidth (MB/s)")
    #ax[plot_index].set_title("c6i_large network bandwidth")
    ax[plot_index].set_xlim(0,xmax-xmin)
    plot_index += 1

    # registered_labels = {}
    # all_starts = []
    # all_finishes = []
    # all_operators = []
    # for file in os.listdir(worker_dir):
    #     full_path = os.path.join(worker_dir, file)
    #     starts, finishes, operators = parse_logs(full_path)
    #     all_starts += [(time - instance_start) / 1000 - xmin for time in starts]
    #     all_finishes += [(time - instance_start) / 1000 - xmin for time in finishes]
    #     all_operators += operators

    # operator_set = set(operators)
    # for operator, i in zip(operator_set, range(0, len(operator_set))):
    #     times = [0]
    #     counts = [0]
    #     events = []

    #     for start, finish, c_operator in zip(all_starts,all_finishes, all_operators):
    #         if operator == c_operator:
    #             events.append((start, "b"))
    #             events.append((finish, "e"))

    #     events = sorted(events)
    #     print(operator, events)
    #     for event in events:
            
    #         counts.append(counts[-1])
    #         times.append(event[0])
    #         times.append(event[0])
    #         if event[1] == "b":
    #             counts.append(counts[-1]+1)
    #         else:
    #             counts.append(counts[-1]-1)
    #     ax[plot_index].plot(times, counts, label=operator, color= cmap(i))
    # ax[plot_index].set_xlabel("Time (s)")
    # ax[plot_index].set_xlim(0,xmax-xmin)
    # ax[plot_index].set_ylabel("Concurrent operators")
    # ax[plot_index].set_title("c6i_large operator activity")

   

    # ax[plot_index].set_xlim(0,xmax-xmin)
    # ax[plot_index].legend()

    # plot_index += 1
    # break
ax[1].set_ylim(0, 1700)
#plot.plot(df["Time"], df["BytesReceived"], color = color)
#plot.plot(df["Time"], df["BytesSend"], color = color)
fig.set_figheight(5)
fig.set_figwidth(4)
fig.tight_layout()
plot.savefig('c6i_usage.png', dpi=300)
plot.show()
    
    