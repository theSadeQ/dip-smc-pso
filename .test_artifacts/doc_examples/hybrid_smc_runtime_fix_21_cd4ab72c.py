# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 21
# Runnable: False
# Hash: cd4ab72c

try:
    result = controller.compute_control(...)
except Exception:
    return "Error occurred"  # Masks the real issue