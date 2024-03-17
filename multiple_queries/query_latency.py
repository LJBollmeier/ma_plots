import matplotlib.pyplot as plt
import numpy as np
import csv

data = {}

with open('latency_results_full.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
    #next(reader, None)
    for row in reader:
        instance_type = row["instance type"]
        if instance_type not in data:
            data[instance_type]=[[],[]]
        data[instance_type][0].append(row["parallel queries"])
        data[instance_type][1].append(float(row["average execution time"]))

# Plotting
plt.figure(figsize=(10, 6))
print(data)

for instance_type, values in data.items():
    plt.plot(values[0][0:15], values[1][0:15], label=instance_type, marker='o')
plt.title('Average Query Execution Time Depending On Number of Parallel Queries')
plt.xlabel('Number of Parallel Queries')
plt.ylabel('Average Execution Time')
plt.legend()
plt.grid(False)
plt.show()

