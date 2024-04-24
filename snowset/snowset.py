import matplotlib.pyplot as plot
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)
cmap = plot.get_cmap("Set2")
import pandas as pd


df = pd.read_csv("snowset/data.csv")
df["time"] = df["time"] / 60

plot.figure(figsize=(5,2.5))
plot.plot(df["time"], df["utilization"], color=cmap(2))
plot.xlabel("Time (m)")
plot.ylabel("Used Cores")
plot.tight_layout()
plot.savefig("snowset", dpi=300)
plot.show()