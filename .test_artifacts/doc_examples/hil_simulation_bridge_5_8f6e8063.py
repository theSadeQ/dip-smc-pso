# Example from: docs\reference\interfaces\hil_simulation_bridge.md
# Index: 5
# Runnable: True
# Hash: 8f6e8063

from src.interfaces.hil.simulation_bridge import SimulationBridge
import time

# Bridge with metrics
bridge = SimulationBridge(
    server_addr=("127.0.0.1", 5555),
    client_addr=("127.0.0.1", 6666)
)

# Metrics collection
metrics = {
    'throughput': [],
    'latency': [],
    'packet_loss': 0
}

# Override message handler for monitoring
original_forward = bridge._forward_message

def monitored_forward(msg, direction):
    start = time.time()
    try:
        result = original_forward(msg, direction)
        latency = (time.time() - start) * 1000
        metrics['latency'].append(latency)
        return result
    except Exception as e:
        metrics['packet_loss'] += 1
        raise

bridge._forward_message = monitored_forward
bridge.start()

# Report metrics
print(f"Mean latency: {np.mean(metrics['latency']):.2f} ms")
print(f"Packet loss: {metrics['packet_loss']} packets")