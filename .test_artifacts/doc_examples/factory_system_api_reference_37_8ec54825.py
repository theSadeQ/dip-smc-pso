# Example from: docs\api\factory_system_api_reference.md
# Index: 37
# Runnable: True
# Hash: 8ec54825

from src.controllers.factory import SMCType, SMC_GAIN_SPECS

# Get gain specification
spec = SMC_GAIN_SPECS[SMCType.CLASSICAL]
print(f"Gain names: {spec.gain_names}")
print(f"Gain bounds: {spec.gain_bounds}")
print(f"Dimension: {spec.n_gains}")