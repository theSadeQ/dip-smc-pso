# Example from: docs\guides\api\utilities.md
# Index: 25
# Runnable: True
# Hash: 00d4745d

from src.utils.monitoring import PerformanceMonitor
from src.utils.analysis import compute_metrics
from src.utils.visualization import plot_results

# Run with monitoring
monitor = PerformanceMonitor(dt=0.01)
monitor.start()

result = runner.run(controller)

# Analyze
metrics = compute_metrics(result)
monitor_stats = monitor.get_statistics()

# Visualize
plot_results(result, show=True)

# Report
print(f"Performance Metrics:")
print(f"  ISE: {metrics['ise']:.4f}")
print(f"  Settling Time: {metrics['settling_time']:.2f} s")
print(f"  Saturation: {monitor_stats['saturation_percentage']:.1f}%")