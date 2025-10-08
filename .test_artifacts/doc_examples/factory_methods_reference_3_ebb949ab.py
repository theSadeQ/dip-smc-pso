# Example from: docs\api\factory_methods_reference.md
# Index: 3
# Runnable: True
# Hash: ebb949ab

# Required gains: [k1, k2, lambda1, lambda2, K, kd]
# Required parameters: max_force, boundary_layer, dt
controller = create_controller(
    'classical_smc',
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
)