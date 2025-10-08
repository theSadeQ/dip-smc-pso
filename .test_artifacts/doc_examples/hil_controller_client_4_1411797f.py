# Example from: docs\reference\interfaces\hil_controller_client.md
# Index: 4
# Runnable: True
# Hash: 1411797f

from src.interfaces.hil import HILControllerClient
import time

# Latency tracking
latencies = []

# Override communication for measurement
original_send_receive = client._send_receive

def measured_send_receive(msg):
    start = time.time()
    result = original_send_receive(msg)
    latency = (time.time() - start) * 1000  # ms
    latencies.append(latency)
    return result

client._send_receive = measured_send_receive
client.run()

# Analyze latencies
print(f"Mean latency: {np.mean(latencies):.2f} ms")
print(f"P95 latency: {np.percentile(latencies, 95):.2f} ms")
print(f"P99 latency: {np.percentile(latencies, 99):.2f} ms")