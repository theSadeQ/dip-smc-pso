# Example from: docs\analysis\HYBRID_SMC_FIX_TECHNICAL_DOCUMENTATION.md
# Index: 4
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