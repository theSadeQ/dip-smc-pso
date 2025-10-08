# Example from: docs\testing\guides\integration_workflows.md
# Index: 3
# Runnable: False
# Hash: 2df00416

# example-metadata:
# runnable: false

def test_config_to_simulation_workflow():
    """Test configuration → controller → simulation pipeline"""
    # Load config
    config = load_config("config.yaml")

    # Create controller from config
    controller = create_controller(
        config['control']['type'],
        config=config['control']['classical_smc']
    )

    # Create dynamics from config
    dynamics = DoublePendulum(
        m1=config['plant']['m1'],
        l1=config['plant']['l1'],
        # ... other params
    )

    # Run simulation
    results = run_simulation(controller, dynamics, config['simulation'])

    # Integration checks
    assert results['success'], "Simulation failed"
    assert 'trajectory' in results, "Missing trajectory data"
    assert results['settling_time'] < 3.0, "Took too long to settle"