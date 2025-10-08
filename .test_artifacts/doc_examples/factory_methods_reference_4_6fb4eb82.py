# Example from: docs\api\factory_methods_reference.md
# Index: 4
# Runnable: True
# Hash: 6fb4eb82

# Required gains: [K1, K2, k1, k2, lambda1, lambda2]
# Required parameters: max_force, dt
controller = create_controller(
    'sta_smc',
    gains=[25.0, 15.0, 20.0, 12.0, 8.0, 6.0]
)