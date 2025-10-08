# Example from: docs\testing\guides\integration_workflows.md
# Index: 4
# Runnable: False
# Hash: 67d0d537

# example-metadata:
# runnable: false

@pytest.fixture
def integrated_system():
    """Fixture providing fully integrated system"""
    config = load_test_config()

    return {
        'controller': create_controller_from_config(config),
        'dynamics': create_dynamics_from_config(config),
        'observer': create_observer_from_config(config),
        'reference': create_reference_from_config(config)
    }

def test_with_integrated_system(integrated_system):
    results = run_closed_loop(integrated_system)
    assert results['tracking_error'] < 0.01