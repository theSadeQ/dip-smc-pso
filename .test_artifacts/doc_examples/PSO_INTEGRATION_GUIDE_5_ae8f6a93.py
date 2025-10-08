# Example from: docs\PSO_INTEGRATION_GUIDE.md
# Index: 5
# Runnable: True
# Hash: ae8f6a93

# Check gain requirements
from src.controllers.factory import SMC_GAIN_SPECS
spec = SMC_GAIN_SPECS[SMCType.CLASSICAL]
print(f"Required gains: {spec.n_gains}")
print(f"Gain names: {spec.gain_names}")

# Validate gains before optimization
gains = [10.0, 5.0, 8.0, 3.0, 15.0, 2.0]
is_valid = validate_smc_gains(SMCType.CLASSICAL, gains)
print(f"Gains valid: {is_valid}")

# Check bounds format
bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
print(f"Bounds format: {type(bounds)}")
print(f"Lower bounds: {bounds[0]}")
print(f"Upper bounds: {bounds[1]}")