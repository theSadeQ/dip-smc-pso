# Example from: docs\guides\how-to\result-analysis.md
# Index: 1
# Runnable: True
# Hash: 651b58c4

import json
import numpy as np

# Load saved results
with open('results_classical.json') as f:
    data = json.load(f)

# Extract metrics
metrics = data['metrics']
print(f"ISE:              {metrics['ise']:.4f}")
print(f"ITAE:             {metrics['itae']:.4f}")
print(f"Settling Time:    {metrics['settling_time']:.2f} s")
print(f"Peak Overshoot:   {metrics['overshoot']:.2f}%")
print(f"Control Effort:   {metrics['control_effort']:.2f}")

# Extract trajectories
time = np.array(data['time'])
state = np.array(data['state'])
control = np.array(data['control'])

# Separate states
cart_pos = state[:, 0]
cart_vel = state[:, 1]
theta1 = state[:, 2]
dtheta1 = state[:, 3]
theta2 = state[:, 4]
dtheta2 = state[:, 5]