# Example from: docs\guides\api\utilities.md
# Index: 1
# Runnable: True
# Hash: 8c9f5296

from src.utils.validation import validate_state

state = np.array([0.1, 0.05, 0.2, 0.1, 0.25, 0.15])

# Basic validation
is_valid = validate_state(state)

# With bounds checking
is_valid = validate_state(
    state,
    x_bounds=(-1.0, 1.0),        # Cart position limits
    theta_bounds=(-0.5, 0.5),    # Angle limits (rad)
    velocity_bounds=(-2.0, 2.0)  # Velocity limits
)

if not is_valid:
    print("State violates constraints!")