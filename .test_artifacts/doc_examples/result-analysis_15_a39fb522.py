# Example from: docs\guides\how-to\result-analysis.md
# Index: 15
# Runnable: True
# Hash: a39fb522

import pandas as pd

# Load data
with open('results_classical.json') as f:
    data = json.load(f)

# Create DataFrame
df = pd.DataFrame({
    'time': data['time'],
    'cart_pos': np.array(data['state'])[:, 0],
    'cart_vel': np.array(data['state'])[:, 1],
    'theta1': np.array(data['state'])[:, 2],
    'dtheta1': np.array(data['state'])[:, 3],
    'theta2': np.array(data['state'])[:, 4],
    'dtheta2': np.array(data['state'])[:, 5],
    'control': data['control']
})

# Save to CSV
df.to_csv('simulation_results.csv', index=False)
print("Exported to simulation_results.csv")