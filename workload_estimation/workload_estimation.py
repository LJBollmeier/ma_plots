import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
cmap = plt.get_cmap("Set2")
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

times = list(range(0, 100))

values = 20 * [8] + 20 * [10] + 20 * [5] + 40 * [10]
values[50] = 15
values[51] = 15
values[52] = 15
values[70] = 15
values[71] = 15
values[72] = 15

# plt.figure(figsize=(4,3))
# plt.xlim(0,100)
# plt.ylim(0,16)
# plt.plot(times, values, color = cmap(0), label = "estimated load")
# plt.xlabel("Time")
# plt.ylabel("Required Cores")
# plt.legend()
# plt.show()

plt.figure(figsize=(5,3))
plt.xlim(0,100)
plt.ylim(0,16)
plt.plot(times, values, color = cmap(0), label = "estimated load")
#plt.plot([0,100], [0,0], color = cmap(1))
divider = [10] * 100
bottom = [0] * 100
plt.savefig("workload_estimation_1", dpi=300)
plt.cla()

plt.fill_between(times, bottom, divider, color=cmap(1), alpha=0.3)
plt.xlim(0,100)
plt.ylim(0,16)
plt.plot(times, values, color = cmap(0), label = "estimated load")
print(len(times), len(bottom), len(divider))
plt.fill_between(times, divider, values, where=[div < val for div, val in zip(divider, values)], color=cmap(5), alpha = 0.3)
plt.xlabel("Time (s)")
plt.ylabel("Cores")
usage_patch = mpatches.Patch(color = cmap(0),alpha = 0.3, label = "estimated")
vs_patch = mpatches.Patch(color = cmap(1), alpha = 0.3, label = "virtual server")
sv_patch = mpatches.Patch(color = cmap(5),alpha = 0.3, label = "serverless")
handles = [usage_patch, vs_patch, sv_patch]
plt.legend(loc = "upper left", handles = handles, bbox_to_anchor=(1,1))
plt.tight_layout()
plt.savefig("workload_estimation_2", dpi=300)
plt.show()
