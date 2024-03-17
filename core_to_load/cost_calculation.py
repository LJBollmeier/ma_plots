import json
import os
from matplotlib import pyplot as plt
cmap = plt.get_cmap("Set2")

def get_warmup_sec():
    return 180

start_ts = 0
def get_start_ts():
    return start_ts + get_warmup_sec() * 1000000000

def request_cost(name, count):
    if name == "S3:HeadObject":
        return 0.0000004 * count
    elif name == "S3:GetObject":
        return 0.0000004 * count
    elif name == "S3:PutObject":
        return 0.000005 * count
    elif name == "S3:ListObjectsV2":
        return 0.000005 * count
    elif name == "SQS:SendMessage":
        return 0.0000004 * count
    elif name == "SQS:ReceiveMessage":
        return 0.0000004 * count
    elif name == "SQS:CreateQueue":
        return 0.0000004 * count
    elif name == "DynamoDB:DescribeTable":
        return 0.00000125 * count
    elif name == "DynamoDB:DescribeEndpoints":
        return 0.00000125 * count
    else:
        return 0.0


def c6i_xl_cost(time_in_s):
    time_in_s = int(time_in_s)
    time_in_s = max(time_in_s, 60)
    price_per_hour = 0.0799
    return price_per_hour / 3600 * time_in_s
    

def get_instance_cost(json):
    js = json["instance_statistics"]
    starts = []
    ends = []
    for instance in js:
        for start, end in zip(instance["start_timestamps"], instance["end_timestamps"]):
            if start < get_start_ts() and end < get_start_ts():
                print("ignored")
                continue

            start = max(start, get_start_ts())
            end = max(end, get_start_ts())
            

            starts.append(int(start) / 1000000000)
            ends.append(int(end) / 1000000000)
    cost = 0.0
    for s,e in zip(starts,ends):
        cost += c6i_xl_cost(e-s)
    return cost

def get_function_cost(js):
    cost = 0.0
    for stats in js:
        if int(stats["approximate_start_ts"]) < get_start_ts():
            continue
        cost += float(stats["cost"])
    return cost

def get_serverless_worker_cost(js):
    return get_function_cost(js["serverless_worker_statistics"])

def get_coordinator_cost(js):
    return get_function_cost(js["coordinator_statistics"])

def get_provisioner_cost(js):
    return get_function_cost(js["pool_manager_statistics"])

def get_request_cost(js):
    qrs = js["query_results"]
    cost = 0.0
    for result in qrs:
        if result["config"]["start_ms"] < (get_warmup_sec() * 1000):
            continue
        # coordinator requests
        coord_stats = result["request_statistics"]
        for k in coord_stats.keys():
            cost += request_cost(k, coord_stats[k]["finished"])
        query_result = result["query_result"]
        pipeline_results = query_result["pipeline_results"]
        for k in pipeline_results.keys():
            request_statistics = pipeline_results[k]["worker_requests"]
            for k2 in request_statistics.keys():
                invocation_request = request_statistics[k2]
                for k3 in invocation_request.keys(): 
                    cost += request_cost(k3, invocation_request[k3]["finished"])
            
    return cost

def plot_costs(name_to_json):
    labels = ["serverless", "instance", "coordinator", "provisioner", "request"]
    
    count = 0
    values = name_to_json.values()
    for js, i in zip(values, range(0,len(values))):
        global start_ts
        start_ts = int(js["start_ts"])
        if count != 0:
            labels = [""] * len(labels)
        costs = [get_serverless_worker_cost(js), get_instance_cost(js), get_coordinator_cost(js), get_provisioner_cost(js), get_request_cost(js)]        
        request_ratio = costs[-1]/ sum(costs) 
        print(js["name"], request_ratio)
        bottom = 0
        for c, j in zip(costs, range(0,len(labels))):
            plt.bar(js["name"], c, label = labels[j], bottom=bottom, color = cmap(j))
            bottom += c
        count += 1
    plt.legend()
    plt.show()
        

result_folder = "core_to_load/results4/"
files = os.listdir(result_folder)
workloads = []
for f in files:
    if ".json" in f:
        workloads.append(result_folder+f)

name_to_json = {}
for w in workloads:
    fd = open(w)
    name_to_json[w] = json.load(fd)

plot_costs(name_to_json)

#fd = open("core_to_load/results3/hybrid_adaptive_3min_warmup2.json")
#fd = open("core_to_load/results3/serverless_3min_warmup.json")
# fd = open("core_to_load/results3/serverful_20_instances_3min_warmup.json")
# #fd = open("core_to_load/results/serverless_2min_warmup.json")
# #fd = open("core_to_load/results/serverful_2min_warmup.json")
# js = json.load(fd)
# start_ts = int(js["start_ts"])
# print(get_serverless_worker_cost(js))
# print(get_instance_cost(js))
# print(get_coordinator_cost(js))
# print(get_provisioner_cost(js))
# print(get_request_cost(js))