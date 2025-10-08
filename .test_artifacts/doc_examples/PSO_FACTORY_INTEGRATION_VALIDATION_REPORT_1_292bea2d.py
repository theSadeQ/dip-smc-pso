# Example from: docs\reports\PSO_FACTORY_INTEGRATION_VALIDATION_REPORT.md
# Index: 1
# Runnable: True
# Hash: 292bea2d

# PSO-Optimized Controller Factory
factory = create_pso_controller_factory(SMCType.CLASSICAL, config)
factory.n_gains = 6
factory.controller_type = 'classical_smc'
factory.max_force = 150.0

# PSOTuner Integration
tuner = PSOTuner(controller_factory=factory, config=config, seed=42)
result = tuner.optimise(iters_override=10, n_particles_override=8)