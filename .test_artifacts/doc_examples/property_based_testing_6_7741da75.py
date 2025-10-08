# Example from: docs\testing\guides\property_based_testing.md
# Index: 6
# Runnable: False
# Hash: 7741da75

# example-metadata:
# runnable: false

@given(
    mass_error=st.floats(min_value=0.8, max_value=1.2),  # ±20%
    friction_error=st.floats(min_value=0.5, max_value=1.5),  # ±50%
    initial_state=valid_states()
)
def test_robust_stabilization(mass_error, friction_error, initial_state):
    """Controller stabilizes despite parameter uncertainties"""
    # Create perturbed dynamics
    perturbed_dynamics = DoublePendulum(
        m1=M1 * mass_error,
        m2=M2 * mass_error,
        b=FRICTION * friction_error
    )

    # Simulate closed-loop
    trajectory = simulate(
        controller, perturbed_dynamics,
        initial_state, duration=5.0
    )

    # Check final state near equilibrium
    final_state = trajectory[-1]
    assert np.linalg.norm(final_state) < 0.1, \
        "Failed to stabilize with parameter errors"