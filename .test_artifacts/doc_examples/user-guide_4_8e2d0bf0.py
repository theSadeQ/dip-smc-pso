# Example from: docs\guides\user-guide.md
# Index: 4
# Runnable: False
# Hash: 8e2d0bf0

# example-metadata:
# runnable: false

# Analyze HIL latency from results
hil_data = json.load(open('hil_results.json'))
latencies = np.array(hil_data['latency_log'])

print(f"Mean Latency: {np.mean(latencies)*1000:.2f} ms")
print(f"Max Latency: {np.max(latencies)*1000:.2f} ms")
print(f"99th Percentile: {np.percentile(latencies, 99)*1000:.2f} ms")

# Plot latency distribution
plt.hist(latencies * 1000, bins=50, edgecolor='black')
plt.xlabel('Latency (ms)')
plt.ylabel('Frequency')
plt.title('HIL Communication Latency Distribution')
plt.grid(axis='y')
plt.show()