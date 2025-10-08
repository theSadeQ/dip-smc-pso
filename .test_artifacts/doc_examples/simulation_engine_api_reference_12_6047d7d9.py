# Example from: docs\api\simulation_engine_api_reference.md
# Index: 12
# Runnable: False
# Hash: 6047d7d9

# Priority hierarchy:
# 1. Explicit u_max parameter
if u_max is not None:
    u_limit = float(u_max)
# 2. Controller's max_force attribute
elif hasattr(controller, 'max_force'):
    u_limit = float(controller.max_force)
# 3. No saturation
else:
    u_limit = None

# Apply saturation
if u_limit is not None:
    u = np.clip(u, -u_limit, u_limit)