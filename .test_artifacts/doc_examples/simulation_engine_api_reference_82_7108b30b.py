# Example from: docs\api\simulation_engine_api_reference.md
# Index: 82
# Runnable: False
# Hash: 7108b30b

# example-metadata:
# runnable: false

monitor = PerformanceMonitor()

monitor.start_timing('simulation')
# ... run simulation ...
elapsed = monitor.end_timing('simulation')

stats = monitor.get_statistics()
# Returns:
# {
#     'simulation': {
#         'count': 100,
#         'total_time': 12.5,
#         'mean_time': 0.125,
#         'std_time': 0.015,
#         'min_time': 0.110,
#         'max_time': 0.180
#     }
# }