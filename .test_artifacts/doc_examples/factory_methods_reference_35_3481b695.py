# Example from: docs\api\factory_methods_reference.md
# Index: 35
# Runnable: False
# Hash: 3481b695

# Horizon must be positive integer
if 'horizon' in params and (not isinstance(params['horizon'], int) or params['horizon'] < 1):
    raise ConfigValueError("horizon must be ≥ 1")

# Geometric constraints
if 'max_cart_pos' in params and params['max_cart_pos'] <= 0:
    raise ConfigValueError("max_cart_pos must be > 0")

# Weight parameters must be non-negative
weight_params = ['q_x', 'q_theta', 'r_u']
for param in weight_params:
    if param in params and params[param] < 0:
        raise ConfigValueError(f"{param} must be ≥ 0")