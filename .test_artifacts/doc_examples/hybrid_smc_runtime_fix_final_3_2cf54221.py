# Example from: docs\troubleshooting\hybrid_smc_runtime_fix_final.md
# Index: 3
# Runnable: True
# Hash: 2cf54221

# Added comprehensive type checking for active_result
if isinstance(active_result, dict):
    control_value = active_result.get('control', 0.0)
elif hasattr(active_result, 'control'):
    control_value = active_result.control
else:
    # Fallback for unexpected types
    control_value = 0.0