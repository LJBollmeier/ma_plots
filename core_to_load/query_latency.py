import os
import matplotlib.pyplot as plt
import json 
import math
import statistics as stat

warmup_ns = 3*60*(10**9)

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

def plot_query_latency_bar(js):
    name = js["name"]
    _, latencies = get_times_and_latencies(js)
    print(latencies)
    plt.bar(name, stat.mean(latencies))


result_folder = "core_to_load/results4/"
files = os.listdir(result_folder)
workloads = []
for f in files:
    if ".json" in f:
        workloads.append(result_folder+f)

for workload in workloads:
    fd = open(workload)
    js = json.load(fd)
    plot_query_latency_bar(js)

plt.show()

