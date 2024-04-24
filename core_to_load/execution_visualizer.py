import json
from matplotlib import pyplot as plt
cmap = plt.get_cmap("Set2")
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)
base_unit = 1000000000
divisor = 1000000
warmup_sec = 180 #180 for hybrid
benchmark_duration = 900


def get_activity(starts, ends):
    print(len(starts))
    if len(starts) == 0:
        return [],[]
    min_start = min(min(starts), min(ends))
    max_end = max(max(starts), max(ends))
    print("range: ",min_start, max_end)


    times = range(int(min_start), int(max_end) + 1)
    values = [0] * len(times)

    for start in starts:
        values[int(start) - int(min_start)] += 1

    for end in ends:
        values[int(end) - int(min_start)] -= 1

    counter = 0

    for v, i in zip(values, range(0, len(values))):
        counter += v
        values[i] = counter
    times = [min(times)] + list(times)
    values = [0] + values
    t2 = []
    v2 = []
    for i in range(1000, len(times), 1000):
        t2.append(times[i])
        v2.append(max(values[i-1000:i+1000]))

    return t2, v2

def get_functions_activity(js):
    starts = []
    ends = []
    for stats in js:
        starts.append(int(stats["approximate_start_ts"]) / divisor)
        ends.append(int(stats["approximate_end_ts"]) / divisor)
    return get_activity(starts, ends)

def get_starts_over_time(js):
    count = 0
    times = []
    starts = []
    for stats in js:
        times.append(int(stats["approximate_start_ts"]) / divisor)
        starts.append(count+1)
        count += 1
    return times, starts

def get_instance_activity(js):
    starts = []
    ends = []
    for instance in js:
        for start in instance["start_timestamps"]:
            starts.append(int(start) / divisor)
        for end in instance["end_timestamps"]:
            ends.append(int(end) / divisor)
    return get_activity(starts, ends)

def get_min(list_of_times):
    min_time = min(list_of_times[0])
    for times in list_of_times:
        min_time = min(min_time, min(times))
    return min_time

def normalize(times, values, m):
    ts = []
    vs = []
    for t,v in zip(times, values):
        if t >= m:
          ts.append((t - m)/ (base_unit/divisor) - warmup_sec)  
          vs.append(v)

    return ts,vs



fd = open("core_to_load/results5/result_4hybrid8.json")
#fd = open("core_to_load/results5/result_5adaptive20.json")
#fd = open("core_to_load/results3/serverless_3min_warmup.json")
#fd = open("core_to_load/results/serverful_2min_warmup.json")
#fd = open("core_to_load/results/serverless_2min_warmup.json")

js = json.load(fd)
serverless_worker_times, serverless_worker_values = get_functions_activity(js["serverless_worker_statistics"])
coordinator_times, coordinator_values = get_functions_activity(js["coordinator_statistics"])
provisioner_times, provisioner_values = get_functions_activity(js["pool_manager_statistics"])
instance_times, instance_values = get_instance_activity(js["instance_statistics"])

tt,ss = get_starts_over_time(js["serverless_worker_statistics"])

# normalize times for plot
relevant_times = []
for t in [serverless_worker_times, coordinator_times, provisioner_times, instance_times]:
    if len(t) > 0:
        relevant_times.append(t)

min_time = min(coordinator_times)
serverless_worker_times, serverless_worker_values = normalize(serverless_worker_times, serverless_worker_values, min_time)
coordinator_times, coordinator_values = normalize(coordinator_times, coordinator_values, min_time)
provisioner_times, provisioner_values = normalize(provisioner_times, provisioner_values, min_time)
instance_times, instance_values = normalize(instance_times, instance_values, min_time)

#plt.plot(tt, ss, label = "worker2")
plt.figure(figsize=(3,3))
plt.xlim(0, benchmark_duration)
plt.plot(instance_times, instance_values, label = "virtual server", color = cmap(0), zorder=2)
plt.xlabel("Time (s)")
plt.ylabel("Active entities")

plt.plot(serverless_worker_times, serverless_worker_values, label = "svl. worker", color = cmap(1), zorder=1)
#plt.plot(coordinator_times, coordinator_values, label = "coordinator", color = cmap(2))
#plt.plot(provisioner_times, provisioner_values, label = "svl. provisioner", color = cmap(3))
plt.tight_layout()
plt.ylim(0,70)
plt.legend()
plt.savefig("eval3_execution_vis", dpi=300)

#plt.ylim(
# 0,25)
plt.show()
