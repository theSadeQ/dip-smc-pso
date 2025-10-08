# Example from: docs\reports\CONTROLLER_TEST_VALIDATION_REPORT.md
# Index: 1
# Runnable: True
# Hash: 54d9c79b

# Fixed constructor signatures in test fixtures
@pytest.fixture(scope="session")
def dynamics(physics_cfg):
    from src.core.dynamics import DIPDynamics
    return DIPDynamics(config=physics_cfg)  # Fixed: was params=physics_cfg