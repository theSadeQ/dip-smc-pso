# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 21
# Runnable: False
# Hash: 50997b1c

# example-metadata:
# runnable: false

try:
    result = controller.compute_control(...)
except Exception:
    return "Error occurred"  # Masks the real issue