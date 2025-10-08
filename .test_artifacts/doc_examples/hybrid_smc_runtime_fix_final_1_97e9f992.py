# Example from: docs\troubleshooting\hybrid_smc_runtime_fix_final.md
# Index: 1
# Runnable: False
# Hash: 97e9f992

# Before Fix - Problematic Flow:
def compute_control(self, state, ...):
    # ... complex control logic ...
    # Missing return statement in some code paths
    # Implicitly returns None

# Downstream Usage:
result = controller.compute_control(state)
# result = None instead of HybridSTAOutput

# Later Processing:
control_value = result.get('control')  # TypeError: None has no attribute 'get'