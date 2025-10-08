# Example from: docs\testing\standards\testing_standards.md
# Index: 2
# Runnable: True
# Hash: 817308a9

from hypothesis import given, strategies as st

@given(
    gains=st.lists(st.floats(min_value=0.1, max_value=100.0), min_size=6, max_size=6),
    state=st.lists(st.floats(min_value=-10.0, max_value=10.0), min_size=6, max_size=6)
)
def test_control_output_bounded_property(gains, state):
    """Property: Control output must always be within actuator limits."""
    controller = ClassicalSMC(gains=gains, max_force=100.0)
    state_array = np.array(state)

    control = controller.compute_control(state_array, 0.0, {})

    assert -100.0 <= control <= 100.0
    assert not np.isnan(control) and not np.isinf(control)

@given(
    initial_state=st.lists(st.floats(min_value=-1.0, max_value=1.0), min_size=6, max_size=6)
)
def test_lyapunov_stability_property(initial_state):
    """Property: Lyapunov function decreases for stable controllers."""
    controller = ClassicalSMC(gains=[10, 8, 15, 12, 50, 5])

    # Simulate short trajectory
    trajectory = simulate_short_trajectory(controller, np.array(initial_state))

    # Compute Lyapunov function
    V_values = [compute_lyapunov_function(state) for state in trajectory]

    # Property: V should generally decrease (allowing for small numerical errors)
    decreasing_trend = np.polyfit(range(len(V_values)), V_values, 1)[0]
    assert decreasing_trend <= 0.01  # Allow small positive slope for numerical stability