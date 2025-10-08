# Example from: docs\plant\models_guide.md
# Index: 16
# Runnable: True
# Hash: 86466974

# Compute energy at initial and current states
E_initial = dynamics.compute_total_energy(state_initial)
E_current = dynamics.compute_total_energy(state_current)

# Energy conservation error
energy_drift = abs(E_current - E_initial) / E_initial

# Validation threshold (accounts for numerical integration error)
assert energy_drift < tolerance, f"Energy drift: {energy_drift:.2%}"