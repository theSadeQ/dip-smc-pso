# Example from: docs\reference\controllers\base_control_primitives.md
# Index: 2
# Runnable: True
# Hash: 6f72a2b3

from src.controllers.base.control_primitives import rate_limit

# Current and previous control
u_current = 80.0
u_previous = 40.0
dt = 0.01  # Time step
u_dot_max = 1000.0  # N/s

# Apply rate limiting
u_limited = rate_limit(u_current, u_previous, u_dot_max, dt)

# Maximum allowed change: 1000 * 0.01 = 10 N
# Requested change: 80 - 40 = 40 N
# Limited change: 10 N
print(f"Rate-limited control: {u_limited:.1f} N")  # 50.0 N