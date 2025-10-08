# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 14
# Runnable: False
# Hash: 38ebc5da

# Complete simulation with PSO-optimized hybrid controller
def run_hybrid_simulation():
    # Load configuration
    config = load_config('config.yaml')

    # Create optimized controller
    controller = create_controller(
        'hybrid_adaptive_sta_smc',
        gains=[77.6216, 44.449, 17.3134, 14.25],  # PSO result
        **config.controllers.hybrid_adaptive_sta_smc
    )

    # Run simulation
    results = run_simulation(
        controller=controller,
        dynamics=dynamics_model,
        duration=10.0,
        dt=0.01
    )

    return results