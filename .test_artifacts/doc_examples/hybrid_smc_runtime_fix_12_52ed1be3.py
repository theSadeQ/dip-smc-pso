# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 12
# Runnable: False
# Hash: 52ed1be3

# example-metadata:
# runnable: false

# Performance timing comparison
timing_results = {
    'before_fix': {
        'compute_control': 'N/A (returned None)',
        'error_handling': '15.3 μs per failure',
        'total_overhead': '~20% PSO slowdown'
    },
    'after_fix': {
        'compute_control': '89.4 μs (normal)',
        'error_handling': '0 μs (no errors)',
        'total_overhead': '0% (optimal performance)'
    }
}