# Example from: docs\factory\enhanced_factory_api_reference.md
# Index: 10
# Runnable: True
# Hash: 4d9b9b28

mpc_params = {
    'horizon': 10,                  # Prediction horizon N
    'q_x': 1.0,                    # State weight (cart position)
    'q_theta': 1.0,                # State weight (pendulum angles)
    'r_u': 0.1,                    # Control weight
    'max_cart_pos': 2.0,           # Position constraint [m]
    'max_force': 150.0             # Control constraint [N]
}