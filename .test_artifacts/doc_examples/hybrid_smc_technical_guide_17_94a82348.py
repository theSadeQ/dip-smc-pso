# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 17
# Runnable: True
# Hash: 94a82348

# Uncertainty handling performance
uncertainties = {
    'mass_variation': ±20%,      # Result: Stable
    'length_variation': ±15%,    # Result: Stable
    'friction_variation': ±50%,  # Result: Stable
    'sensor_noise': 0.1° RMS,    # Result: Robust
    'actuator_delay': 5ms,       # Result: Acceptable
}