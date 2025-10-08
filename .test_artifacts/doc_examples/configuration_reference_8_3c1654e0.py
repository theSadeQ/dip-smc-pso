# Example from: docs\factory\configuration_reference.md
# Index: 8
# Runnable: False
# Hash: 3c1654e0

# example-metadata:
# runnable: false

# Hybrid controller requires sub-configurations
classical_config = ClassicalSMCConfig(
    gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0],
    max_force=150.0, dt=0.001, boundary_layer=0.02
)
adaptive_config = AdaptiveSMCConfig(
    gains=[12.0, 10.0, 6.0, 5.0, 2.5],
    max_force=150.0, dt=0.001
)

config_params = {
    'hybrid_mode': HybridMode.CLASSICAL_ADAPTIVE,
    'dt': 0.001,
    'max_force': 150.0,
    'classical_config': classical_config,
    'adaptive_config': adaptive_config,
    'dynamics_model': dynamics_model
}