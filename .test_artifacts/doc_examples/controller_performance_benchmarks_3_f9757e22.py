# Example from: docs\benchmarks\controller_performance_benchmarks.md
# Index: 3
# Runnable: True
# Hash: f9757e22

import pandas as pd

# Load performance data
df = pd.read_csv('controller_performance_summary.csv')

# Find fastest computation
fastest = df.loc[df['computation_avg'].idxmin()]
print(f"Fastest controller: {fastest['controller']} ({fastest['computation_avg']:.4f} ms)")

# Compare Classical vs Hybrid
classical = df[df['controller'] == 'classical_smc'].iloc[0]
hybrid = df[df['controller'] == 'hybrid_adaptive_sta_smc'].iloc[0]
speedup = hybrid['computation_avg'] / classical['computation_avg']
print(f"Classical is {speedup:.1f}× faster than Hybrid")