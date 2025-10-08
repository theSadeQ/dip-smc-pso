# Example from: docs\testing\guides\property_based_testing.md
# Index: 7
# Runnable: True
# Hash: ecd5e385

from hypothesis import strategies as st

def valid_states(
    theta_max=π,
    velocity_max=10,
    constrain_to_basin=False
):
    """Generate valid state vectors"""
    if constrain_to_basin:
        # Only generate states in region of attraction
        theta_strategy = st.floats(min_value=-0.5, max_value=0.5)
    else:
        # Full state space
        theta_strategy = st.floats(
            min_value=-theta_max,
            max_value=theta_max,
            allow_nan=False,
            allow_infinity=False
        )

    velocity_strategy = st.floats(
        min_value=-velocity_max,
        max_value=velocity_max,
        allow_nan=False
    )

    return st.tuples(
        theta_strategy,  # theta1
        theta_strategy,  # theta2
        velocity_strategy,  # dtheta1
        velocity_strategy   # dtheta2
    )