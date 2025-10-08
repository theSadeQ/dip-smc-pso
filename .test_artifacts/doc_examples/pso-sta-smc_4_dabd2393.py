# Example from: docs\guides\workflows\pso-sta-smc.md
# Index: 4
# Runnable: True
# Hash: dabd2393

# Add constraint to PSO
# Ensure K2 > 0.5·K1 during optimization

# Or post-process gains
if K2 < 0.5 * K1:
    K2 = 0.55 * K1  # Add 10% safety margin