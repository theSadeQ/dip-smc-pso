# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 16
# Runnable: False
# Hash: 20fb0f72

# Complete simulation with classical SMC
def run_classical_smc_simulation():
    # Load configuration
    config = load_config('config.yaml')

    # Create dynamics
    dynamics = DoubleInvertedPendulum(params=config.physics)

    # Create controller
    controller = create_controller(
        'classical_smc',
        gains=config.controllers.classical_smc.gains,
        max_force=config.controllers.classical_smc.max_force,
        boundary_layer=config.controllers.classical_smc.boundary_layer,
        dynamics_model=dynamics
    )

    # Run simulation
    results = run_simulation(
        controller=controller,
        dynamics=dynamics,
        duration=10.0,
        dt=0.01,
        initial_state=config.simulation.initial_state
    )

    return results