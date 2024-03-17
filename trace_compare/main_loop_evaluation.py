from matplotlib import pyplot as plt
import csv

times = []
ids = []

with open("trace_compare/logs_detailed") as fd:
    lines = csv.reader(fd,)
    next(lines)
    for line in lines:
        times.append(int(line[0]))
        ids.append(line[1])

identifiers = []
diffs = []
for i in range(1, (len(times)-1)):
    diffs.append((times[i+1]-times[i]) / (10**6))
    identifiers.append(ids[i+1])

iteration = range(0, len(diffs))
max_val = 0
max_id = ""
max_index = 0
id_map = {}
x_min = 646200
x_max = 646470

idxs = range(2,len(identifiers)+2)
for id,time,idx in zip(identifiers,diffs, idxs):
    if (idx < x_min or idx > x_max):
        continue
    if not id in id_map:
        id_map[id] = time
    else:
        id_map[id] += time
    if time > max_val:
        max_val = time
        max_id = id
        max_index = idx

print("Time:", (times[x_max]-times[x_min]) / 10**6)
print(id_map)

print(max_id, max_val, max_index)


ax = plt.subplot()


ax.plot(iteration, diffs)
ax.set_xlim(x_min, x_max)
#print(sum(diffs[198300:202000])-((202000-198300)*0.1))
#print((times[202000]-times[198300])/(10**6))
plt.show()