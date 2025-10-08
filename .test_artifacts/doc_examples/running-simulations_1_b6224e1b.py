# Example from: docs\guides\how-to\running-simulations.md
# Index: 1
# Runnable: True
# Hash: b6224e1b

import json

# Load results
with open('baseline.json') as f:
    data = json.load(f)

# Access metrics
print(f"ISE: {data['metrics']['ise']:.4f}")
print(f"Settling Time: {data['metrics']['settling_time']:.2f}s")

# Access controller type
print(f"Controller: {data['controller_type']}")

# Access gains used
print(f"Gains: {data['gains']}")