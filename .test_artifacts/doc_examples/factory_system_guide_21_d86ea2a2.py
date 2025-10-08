# Example from: docs\controllers\factory_system_guide.md
# Index: 21
# Runnable: False
# Hash: d86ea2a2

# Enterprise Factory
controller = create_controller(
    controller_type='classical_smc',
    config=config,
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0]  # [k1, k2, λ1, λ2, K, kd]
)

# Clean SMC Factory
controller = SMCFactory.create_from_gains(
    smc_type=SMCType.CLASSICAL,
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
    max_force=100.0,
    dt=0.01,
    boundary_layer=0.02
)

# Internal creation (ClassicalSMC constructor)
controller = ClassicalSMC(
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
    max_force=100.0,
    boundary_layer=0.02,
    dynamics_model=dynamics_model
)