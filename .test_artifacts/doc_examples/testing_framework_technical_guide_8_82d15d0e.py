# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 8
# Runnable: True
# Hash: 82d15d0e

@pytest.fixture
def initial_state():
    """Standard initial state for testing: small perturbation from equilibrium."""
    return np.array([0.0, 0.0, 0.1, 0.1, 0.0, 0.0])

@pytest.fixture
def controller_gains_classical():
    """Standard classical SMC gains for testing."""
    return [10.0, 8.0, 15.0, 12.0, 50.0, 5.0]

@pytest.fixture
def make_classical_controller(controller_gains_classical):
    """Factory fixture for creating classical SMC controllers."""
    def _make(**kwargs):
        from src.controllers.smc.classic_smc import ClassicalSMC
        default_params = {
            'gains': controller_gains_classical,
            'max_force': 100.0,
            'boundary_layer': 0.01,
            'dt': 0.01
        }
        default_params.update(kwargs)
        return ClassicalSMC(**default_params)
    return _make

@pytest.fixture
def simulation_params():
    """Standard simulation parameters for testing."""
    return {
        'duration': 5.0,
        'dt': 0.01,
        'max_force': 100.0
    }