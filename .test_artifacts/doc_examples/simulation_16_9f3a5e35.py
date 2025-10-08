# Example from: docs\guides\api\simulation.md
# Index: 16
# Runnable: True
# Hash: 9f3a5e35

# Enable detailed logging
context.enable_logging(level='DEBUG', log_file='simulation.log')

# Monitor performance
context.start_performance_monitor()
result = runner.run(controller)
perf_stats = context.get_performance_stats()

print(f"Execution time: {perf_stats['total_time']:.3f}s")
print(f"Average timestep: {perf_stats['avg_step_time']:.6f}s")