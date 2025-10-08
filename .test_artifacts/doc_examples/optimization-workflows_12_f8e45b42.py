# Example from: docs\guides\how-to\optimization-workflows.md
# Index: 12
# Runnable: True
# Hash: f8e45b42

# Verify bounds allow good solutions
print("Parameter bounds:")
for i, bounds in enumerate(config.pso.bounds):
    print(f"  Gain {i+1}: [{bounds[0]}, {bounds[1]}]")