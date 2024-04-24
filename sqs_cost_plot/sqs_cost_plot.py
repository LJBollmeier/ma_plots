import matplotlib.pyplot as plt
cmap = plt.get_cmap("Set2")
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

# c6i large instance, two fragments
instance_cost_on_demand = 0.085 / 3600 / 1000 / 2
instance_cost_spot = 0.036 / 3600 / 1000 / 2
instance_cost_serverless = 0.0000166667 / 1024 * 1769 / 1000

message_cost_serverless = 0.00000040 * 4
message_cost_serverful = 0.00000040 * 6

min_time_ms = 100
max_time_ms = 3100
time_step = 100

times = list(range(min_time_ms, max_time_ms, time_step))
cost_on_demand = [message_cost_serverful / (t * instance_cost_on_demand) for t in times]
cost_spot = [message_cost_serverful / (t * instance_cost_spot) for t in times]
cost_serverless = [message_cost_serverless / (t * instance_cost_serverless) for t in times]
for t,c in zip(times, cost_spot):
    print(t,c)

plt.figure(figsize=(4,3))
plt.plot(times, cost_on_demand, color = cmap(0), label = "on demand")
plt.plot(times, cost_spot, color = cmap(1), label = "spot")
plt.plot(times, cost_serverless, color = cmap(2), label = "serverless")
plt.xlabel("Fragment execution time (ms)")
plt.ylabel("Message cost / compute costs")
plt.legend()
plt.tight_layout()
plt.savefig("sqs_cost", dpi = 300)
plt.show()