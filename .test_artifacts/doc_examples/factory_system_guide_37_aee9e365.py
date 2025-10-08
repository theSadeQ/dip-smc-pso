# Example from: docs\controllers\factory_system_guide.md
# Index: 37
# Runnable: True
# Hash: aee9e365

# Solution: Ensure wrapper extracts control value correctly
if hasattr(result, 'u'):
    control_value = result.u
elif isinstance(result, dict) and 'u' in result:
    control_value = result['u']
else:
    control_value = result  # Fallback