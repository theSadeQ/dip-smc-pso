# Example from: docs\reference\plant\models_base_dynamics_interface.md
# Index: 6
# Runnable: True
# Hash: 172b213c

from src.plant.models.simplified import SimplifiedDIPDynamics

# Enable numerical stability features
dynamics = SimplifiedDIPDynamics(
    config=config,
    enable_energy_monitoring=True,
    numerical_tolerance=1e-8,
    use_numba=True  # JIT compilation for performance
)

# Configure integration parameters
dynamics.set_integration_params(
    method='rk45',
    atol=1e-8,
    rtol=1e-6
)