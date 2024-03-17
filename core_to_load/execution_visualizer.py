import json
from matplotlib import pyplot as plt

def get_activity(starts, ends):
    print(len(starts))
    if len(starts) == 0:
        return [],[]
    min_start = min(min(starts), min(ends))
    max_end = max(max(starts), max(ends))

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
    return times, values

def get_functions_activity(js):
    starts = []
    ends = []
    for stats in js:
        starts.append(int(stats["approximate_start_ts"]) / 1000000000)
        ends.append(int(stats["approximate_end_ts"]) / 1000000000)
    return get_activity(starts, ends)
    

def get_instance_activity(js):
    starts = []
    ends = []
    for instance in js:
        for start in instance["start_timestamps"]:
            starts.append(int(start) / 1000000000)
        for end in instance["end_timestamps"]:
            ends.append(int(end) / 1000000000)
    return get_activity(starts, ends)

def get_min(list_of_times):
    min_time = min(list_of_times[0])
    for times in list_of_times:
        min_time = min(min_time, min(times))
    return min_time

def normalize(times, m):
    l = [(t - m) for t in times]
    return l



fd = open("core_to_load/results4/adaptive_hybrid.json")
#fd = open("core_to_load/results3/serverless_3min_warmup.json")
#fd = open("core_to_load/results/serverful_2min_warmup.json")
#fd = open("core_to_load/results/serverless_2min_warmup.json")

js = json.load(fd)
serverless_worker_times, serverless_worker_values = get_functions_activity(js["serverless_worker_statistics"])
coordinator_times, coordinator_values = get_functions_activity(js["coordinator_statistics"])
provisioner_times, provisioner_values = get_functions_activity(js["pool_manager_statistics"])
instance_times, instance_values = get_instance_activity(js["instance_statistics"])

# normalize times for plot
relevant_times = []
for t in [serverless_worker_times, coordinator_times, provisioner_times, instance_times]:
    if len(t) > 0:
        relevant_times.append(t)

min_time = get_min(relevant_times)
serverless_worker_times = normalize(serverless_worker_times, min_time)
coordinator_times = normalize(coordinator_times, min_time)
provisioner_times = normalize(provisioner_times, min_time)
instance_times = normalize(instance_times, min_time)

plt.plot(serverless_worker_times, serverless_worker_values, label = "worker")
plt.plot(provisioner_times, provisioner_values, label = "provisioner")
plt.plot(coordinator_times, coordinator_values, label = "coordinator")
plt.plot(instance_times, instance_values, label = "instance")
plt.legend()
#plt.xlim(50, 260)
#plt.ylim(
# 0,25)
plt.show()
