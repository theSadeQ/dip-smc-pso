# Example from: docs\api\factory_methods_reference.md
# Index: 6
# Runnable: True
# Hash: 1f712b79

# Required gains: [k1, k2, lambda1, lambda2]
# Special handling: Creates sub-controllers automatically
controller = create_controller(
    'hybrid_adaptive_sta_smc',
    gains=[18.0, 12.0, 10.0, 8.0]
)