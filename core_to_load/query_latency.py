import os
import matplotlib.pyplot as plt
import json 
import numpy
import math
import statistics as stat
import matplotlib.patches as mpatches
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

warmup_ns = 3*60*(10**9)
last_phase_start = warmup_ns + 10 * 60 * (10 ** 9)
first_phase_end = warmup_ns + 5 * 60 * (10 ** 9)
cmap = plt.get_cmap("Set2")

def get_times_and_latencies(js):
    starts_ts = int(js["start_ts"])
    benchmark_begin = starts_ts + warmup_ns
    query_results = js["query_results"]
    times = []
    latencies = []

    for q in query_results:
        query_start = int(q["config"]["start_ms"])
        if query_start* 10**6 + starts_ts < benchmark_begin:
            continue
        query_latency = int(q["query_result"]["execution_duration_ms"])
        times.append(query_start)
        latencies.append(query_latency)
    return times, latencies

def plot_query_latency_bar(js, sp):
    name = js["name"]
    times, latencies = get_times_and_latencies(js)

    latencies_phase_1 = []
    for t,l in zip(times,latencies):
        if t * (10**6) <= first_phase_end:
            latencies_phase_1.append(l)

    latencies_phase_3 = []
    for t,l in zip(times,latencies):
        if t * (10**6) > last_phase_start:
            latencies_phase_3.append(l)

    mean = stat.mean(latencies)
    print(name,mean, numpy.percentile(latencies, 95), stat.mean(latencies_phase_1), stat.mean(latencies_phase_3))
    sp.bar(name, mean, color = cmap(0))

def plot_query_latency_bar_with_perc(js, sp):
    name = js["name"]
    _, latencies = get_times_and_latencies(js)
    mean = stat.mean(latencies)
    perc = numpy.percentile(latencies, 95)
    sp.bar(name, mean, color = cmap(0))
    sp.bar(name, perc-mean, bottom=mean, color=cmap(1))    
    
fig, ax = plt.subplots(1,2)

mean_patch = mpatches.Patch(color = cmap(0), label = "average")
perc_patch = mpatches.Patch(color = cmap(1), label = "95th percentile")

result_folder = "core_to_load/results5/"
files = os.listdir(result_folder)
workloads = []
for f in files:
    if ".json" in f:
        workloads.append(result_folder+f)
workloads = sorted(workloads)

for workload in workloads:
    fd = open(workload)
    js = json.load(fd)
    plot_query_latency_bar(js, ax[0])
ax[0].set_ylabel("Query execution time (ms)")
ax[0].legend(loc = "upper right", handles = [mean_patch])

for workload in workloads:
    fd = open(workload)
    js = json.load(fd)
    if js["name"] == "vs8":
        continue
    plot_query_latency_bar_with_perc(js, ax[1])


ax[1].set_ylabel("Query execution time (ms)")
ax[0].set_xlabel("System configuration")
ax[1].set_xlabel("System configuration")
ax[1].legend(loc = "lower left", handles = [mean_patch, perc_patch])
fig.tight_layout()
fig.set_figheight(2)
fig.set_figwidth(6)
fig.savefig("eval3_latency", dpi=300, bbox_inches="tight")
plt.show()

