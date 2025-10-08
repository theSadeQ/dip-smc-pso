# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 23
# Runnable: True
# Hash: 8656f454

# Create both controllers directly
stabilizer = create_controller('sta_smc', config=config)

swing_up = SwingUpSMC(
    dynamics_model=dynamics,
    stabilizing_controller=stabilizer,
    energy_gain=50.0
)