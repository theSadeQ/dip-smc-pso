# Example from: docs\reports\test_infrastructure_analysis_report.md
# Index: 5
# Runnable: True
# Hash: a775febd

@pytest.fixture(scope="session")
def config()              # Complete configuration loading
def physics_cfg(config)   # Physics configuration extraction
def physics_params()      # Backward compatibility alias
def dynamics()            # Simplified DIP dynamics
def full_dynamics()       # Full nonlinear dynamics
def long_simulation_config()  # Long simulation toggle