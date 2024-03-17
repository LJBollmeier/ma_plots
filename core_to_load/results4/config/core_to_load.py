import matplotlib.pyplot as plot
import random as rnd
import math
import statistics
rnd.seed(1337)

duration = 15 * 60 * 1000
max_cores = 50
query_length = 2000
required_cores_per_query = 10
warmup_duration = 3 * 60 * 1000

times = list(range(0,duration + 1))
values = [0] * len(times)

# step one: Generate base utilization
sustained_load_count = 3
part_length = int(duration/sustained_load_count)
for i in range(0, sustained_load_count):
    load = 0.0
    if i == 0:
        load = 0.5 * max_cores
    if i == 1 :
        load = 0
    if i == 2:
        load = max_cores

    for j in range(part_length * i, part_length * (i+1)):
        values[j] += load

burst_probability_per_second = 0.05
burst_duration = 2000 + int(rnd.random() * 6000)
max_burst_height = max_cores / 2

# step two: add bursts
for i in range(0, len(values)):
    if rnd.random() <= burst_probability_per_second / 1000:
        #print("burst")
        burst_height = rnd.random() * max_burst_height
        #print(burst_height)
        for j in range(i, min(len(values), i + burst_duration)):
            values[j] += burst_height

# step three: generate zeros

for i in range(0, len(values)):
    if i >= 1  * part_length and i < 2 * part_length:
        values[i] = 0
    # if rnd.random() <= zero_probability_per_second / 1000:
    #     print("zero")
    #     for j in range(i, min(i + zero_duration, len(values))):
    #         values[j] = 0

# step X: add warmup phase
avg_value = statistics.mean(values)
print("average:", avg_value)
times = times + list(range(len(times), len(times) + warmup_duration))
values = [avg_value] * warmup_duration + values

# step four: generate query stream
    #cut everything in parts of query length and get average of a slice.
slice_length = query_length
slices_count = int(len(times) / query_length)
qt = []
qv = []

for slice in range(0, slices_count):
    sumc = 0
    count = 0
    for v in values[slice * slice_length: (slice + 1) * slice_length]:
        sumc += v
        count +=1
    qt.append(slice * slice_length)
    qv.append(math.ceil(sumc/count / required_cores_per_query))

queries_until_zero = 0

for i in range(0, len(qv)-1):
    queries_until_zero += qv[i]
    if qv[i+1] == 0 :
        break

print("queries until zero: ", queries_until_zero)

query_count =  sum(qv)
print("number of queries: ", query_count)

# step five: Fit stream into json
json_string = '{"query_stream": ['
for t,v in zip(qt, qv):
    for i in range(0,v):
        json_object = '''
        {
            "compiler_config": {
                "compiler_type": "kTpch",
                "query": "kQ6",
                "scale_factor": "kSF10",
                "working_directory": {
                    "bucket": "skyrise-ci",
                    "identifier": "testNgUWf",
                    "etag": ""
                }
            },
            "start_ms":'''
        json_object += str(t)
        json_object += '},' 
        json_string += json_object
json_string = json_string[0:-1]
json_string += ']}'

fd = open("tpch_stream.json", "w")
fd.write(json_string)

plot.plot(times, values)
plot.plot(qt, qv)

plot.set_xlabel = "Time (s)"
plot.set_ylabel = "Cores used"
#plot.xlim(50000,260000)
plot.show()
