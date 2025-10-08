# Example from: docs\guides\workflows\hil-workflow.md
# Index: 3
# Runnable: True
# Hash: 56d0e90b

import numpy as np

data = np.load('out/hil_results.npz', allow_pickle=True)
meta = data['meta'].item()

# Network configuration
print(f"Plant: {meta['plant_ip']}:{meta['plant_port']}")
print(f"Controller: {meta['controller_ip']}:{meta['controller_port']}")
print(f"Control loop rate: {1/meta['dt']:.0f} Hz")
print(f"Total steps: {meta['steps']}")

# Data integrity check
t = data['t']
x = data['x']
u = data['u']

print(f"\nData Integrity:")
print(f"  Time points: {len(t)} (expected {meta['steps']+1})")
print(f"  State samples: {x.shape[0]} (expected {meta['steps']+1})")
print(f"  Control samples: {u.shape[0]} (expected {meta['steps']})")
print(f"  NaN in state: {np.isnan(x).any()}")
print(f"  NaN in control: {np.isnan(u).any()}")
print(f"  Inf in state: {np.isinf(x).any()}")
print(f"  Inf in control: {np.isinf(u).any()}")

# Timing analysis
dt_actual = np.diff(t)
dt_mean = dt_actual.mean()
dt_std = dt_actual.std()
print(f"\nTiming Analysis:")
print(f"  Target dt: {meta['dt']:.4f} s")
print(f"  Actual dt (mean): {dt_mean:.4f} s")
print(f"  Actual dt (std): {dt_std:.6f} s")
print(f"  Timing jitter: {dt_std/dt_mean*100:.2f}%")