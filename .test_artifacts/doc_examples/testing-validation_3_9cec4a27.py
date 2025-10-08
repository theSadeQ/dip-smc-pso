# Example from: docs\guides\how-to\testing-validation.md
# Index: 3
# Runnable: True
# Hash: 9cec4a27

# In conftest.py
import pytest
from src.config import load_config

@pytest.fixture
def config():
    """Load test configuration."""
    return load_config('config.yaml')

@pytest.fixture
def classical_controller(config):
    """Create classical SMC controller."""
    from src.controllers import create_smc_for_pso, SMCType
    return create_smc_for_pso(
        SMCType.CLASSICAL,
        gains=[10, 8, 15, 12, 50, 5],
        max_force=100.0
    )

# In test file
def test_with_fixture(classical_controller):
    """Test using pre-configured controller."""
    state = np.array([0, 0, 0.1, 0, 0.15, 0])
    control, _, _ = classical_controller.compute_control(state, {}, {})
    assert abs(control) <= 100.0