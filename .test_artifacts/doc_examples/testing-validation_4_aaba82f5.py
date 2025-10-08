# Example from: docs\guides\how-to\testing-validation.md
# Index: 4
# Runnable: True
# Hash: aaba82f5

# tests/test_integration/test_end_to_end.py
def test_full_simulation():
    """Test complete simulation workflow."""
    from src.controllers.factory import create_controller
    from src.core.simulation_runner import SimulationRunner
    from src.config import load_config

    # Load config
    config = load_config('config.yaml')

    # Create controller
    controller = create_controller(
        'classical_smc',
        config=config.controllers.classical_smc
    )

    # Run simulation
    runner = SimulationRunner(config)
    result = runner.run(controller)

    # Validate results
    assert 'metrics' in result
    assert 'time' in result
    assert 'state' in result
    assert 'control' in result

    # Check stability (state remains bounded)
    state = np.array(result['state'])
    assert np.all(np.abs(state) < 10.0), "State diverged"

    # Check settling time reasonable
    assert result['metrics']['settling_time'] < 10.0