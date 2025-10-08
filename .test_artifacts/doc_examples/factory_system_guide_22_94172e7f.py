# Example from: docs\controllers\factory_system_guide.md
# Index: 22
# Runnable: False
# Hash: 94172e7f

# example-metadata:
# runnable: false

# Clean SMC Factory
controller = SMCFactory.create_from_gains(
    smc_type=SMCType.ADAPTIVE,
    gains=[25.0, 18.0, 15.0, 10.0, 4.0],  # [k1, k2, λ1, λ2, γ]
    max_force=100.0,
    dt=0.01,
    leak_rate=0.1,
    adapt_rate_limit=100.0,
    K_min=0.1,
    K_max=100.0,
    K_init=10.0
)

# Internal creation (AdaptiveSMC constructor)
controller = AdaptiveSMC(
    gains=[25.0, 18.0, 15.0, 10.0, 4.0],
    dt=0.01,
    max_force=100.0,
    leak_rate=0.1,
    adapt_rate_limit=100.0,
    K_min=0.1,
    K_max=100.0,
    smooth_switch=True,
    boundary_layer=0.01,
    dead_zone=0.05
)