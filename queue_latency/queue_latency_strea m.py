import matplotlib.pyplot as plot
import random as rnd
import math
import statistics
rnd.seed(1337)

duration = 300000
slots = 2
query_latency = 1500
overloading = 2

query_frequency = query_latency / slots / overloading

latencies = [t for t in range(0, duration, int(query_frequency))]
print(len(latencies))

# step five: Fit stream into json
json_string = '{"query_stream": ['
for t in latencies:
        json_object = '''
        {
            "compiler_config": {
                "compiler_type": "kTpch",
                "query": "kQ6",
                "scale_factor": "kSF1",
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
