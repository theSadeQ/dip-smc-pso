# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 18
# Runnable: False
# Hash: cfe98d69

# example-metadata:
# runnable: false

# Performance profiling results
computation_times = {
    'sliding_surface': '12.3 μs',      # Fast
    'adaptive_gains': '18.7 μs',       # Moderate
    'equivalent_control': '45.2 μs',   # Expensive (matrix ops)
    'total_per_step': '89.4 μs',      # Real-time capable at 1kHz
}

# Memory usage
memory_footprint = {
    'controller_object': '2.1 KB',
    'history_storage': '15.6 KB/minute',
    'peak_simulation': '156 MB',       # Including visualization
}