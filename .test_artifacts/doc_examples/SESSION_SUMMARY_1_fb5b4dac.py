# Example from: docs\SESSION_SUMMARY.md
# Index: 1
# Runnable: False
# Hash: fb5b4dac

# example-metadata:
# runnable: false

# Original (WRONG):
fitness = tracking_error_rms + chattering_penalty + ...
# chattering_penalty = 0 if chattering < 2.0 ← ALWAYS ZERO!

# Corrected (RIGHT):
fitness = chattering_index  # Direct minimization