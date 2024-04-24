import matplotlib.pyplot as plt

# Data
queue_size = ["0", "1", "2", "5", "10", "20", "1000"]
average_latency = [1507, 1847, 2194, 3282, 5181, 8965, 135658]
percentile_90th = [1784, 2224, 2827, 5440, 9034, 16658, 246277]

# Plot
fig, ax = plt.subplots()

# Plot the average latencies
ax.bar(queue_size, average_latency, label='Average Latency')

# Plot the 90th percentile on top of the average latency
ax.bar(queue_size, percentile_90th, bottom=average_latency, label='90th Percentile')

# Set y-axis break
ax.set_ylim(0, 15000)  # adjust the limits as per your preference
ax.spines['bottom'].set_visible(False)  # hide bottom spine

# Add a break in the y-axis
ax.plot([100, 100], [0, 15000], color='black', linestyle='--', linewidth=1)
ax.plot([0, 100], [15000, 15000], color='black', linestyle='--', linewidth=1)

# Labeling and styling
ax.set_xlabel('Queue Size')
ax.set_ylabel('Latency')
ax.set_title('Latency Analysis')
ax.legend()
plt.xticks(queue_size)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

plt.show()