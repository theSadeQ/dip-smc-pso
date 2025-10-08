# Example from: docs\guides\how-to\optimization-workflows.md
# Index: 13
# Runnable: False
# Hash: ca455bdf

# example-metadata:
# runnable: false

# Check gains for physical plausibility
with open('optimized_gains.json') as f:
    gains = json.load(f)['gains']

print("Optimized gains:")
print(f"  k1 (should be positive): {gains[0]:.2f}")
print(f"  k2 (should be positive): {gains[1]:.2f}")
print(f"  λ1 (should be positive): {gains[2]:.2f}")
print(f"  λ2 (should be positive): {gains[3]:.2f}")
print(f"  K (should be >> 0):      {gains[4]:.2f}")
print(f"  ε (should be small):     {gains[5]:.4f}")

# If gains are at bounds, widen search