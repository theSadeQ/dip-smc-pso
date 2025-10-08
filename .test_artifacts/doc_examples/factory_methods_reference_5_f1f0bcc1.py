# Example from: docs\api\factory_methods_reference.md
# Index: 5
# Runnable: True
# Hash: f1f0bcc1

# Required gains: [k1, k2, lambda1, lambda2, gamma]
# Required parameters: max_force, dt
controller = create_controller(
    'adaptive_smc',
    gains=[25.0, 18.0, 15.0, 10.0, 4.0]
)