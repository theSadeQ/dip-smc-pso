# Example from: docs\reference\interfaces\hil_plant_server.md
# Index: 5
# Runnable: True
# Hash: 21a635f0

from src.interfaces.hil import PlantServer
import time
import psutil

# Metrics collection
metrics = {
    'step_times': [],
    'memory_usage': [],
    'cpu_usage': []
}

# Custom server with profiling
server = PlantServer(cfg=config, bind_addr=("127.0.0.1", 5555), dt=0.01)

# Override step function for profiling
original_step = server._step
def profiled_step(control):
    start = time.time()
    result = original_step(control)
    metrics['step_times'].append(time.time() - start)
    metrics['memory_usage'].append(psutil.Process().memory_info().rss / 1024**2)
    metrics['cpu_usage'].append(psutil.cpu_percent())
    return result

server._step = profiled_step
server.start()
server.close()

# Analyze performance
print(f"Mean step time: {np.mean(metrics['step_times']):.4f} s")
print(f"Max memory: {max(metrics['memory_usage']):.1f} MB")
print(f"Mean CPU: {np.mean(metrics['cpu_usage']):.1f}%")