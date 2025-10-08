# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 16
# Runnable: False
# Hash: adce5a66

# This will raise ValueError:
SwingUpSMC(
    ...,
    switch_energy_factor=0.95,
    exit_energy_factor=0.98  # ERROR: exit ≥ switch
)