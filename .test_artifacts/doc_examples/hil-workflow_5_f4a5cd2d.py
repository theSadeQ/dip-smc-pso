# Example from: docs\guides\workflows\hil-workflow.md
# Index: 5
# Runnable: True
# Hash: f4a5cd2d

# Real-time monitoring script
import numpy as np
import time

while True:
    try:
        data = np.load('out/hil_results.npz', allow_pickle=True)
        u = data['u']

        # Check control limits
        u_max = np.max(np.abs(u))
        if u_max > 100:  # Force limit
            print(f"WARNING: Control force {u_max:.2f}N exceeds limit!")

        time.sleep(1.0)
    except FileNotFoundError:
        pass