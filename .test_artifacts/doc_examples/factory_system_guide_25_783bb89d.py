# Example from: docs\controllers\factory_system_guide.md
# Index: 25
# Runnable: True
# Hash: 783bb89d

# List available controllers
available = list_available_controllers()
# ['classical_smc', 'sta_smc', 'adaptive_smc', 'hybrid_adaptive_sta_smc']

# Get controller metadata
spec = SMC_GAIN_SPECS[SMCType.CLASSICAL]
print(f"Controller: {spec.description}")
print(f"Gains: {spec.gain_names}")
print(f"Count: {spec.n_gains}")