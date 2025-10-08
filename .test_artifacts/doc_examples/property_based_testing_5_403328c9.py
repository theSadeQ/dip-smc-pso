# Example from: docs\testing\guides\property_based_testing.md
# Index: 5
# Runnable: False
# Hash: 403328c9

# example-metadata:
# runnable: false

@given(
    state=valid_states(),
    perturbation=st.floats(min_value=-0.01, max_value=0.01)
)
def test_control_continuity(state, perturbation):
    """Control law is Lipschitz continuous"""
    u1 = controller.compute_control(state)

    perturbed_state = state + perturbation
    u2 = controller.compute_control(perturbed_state)

    # Control change bounded by Lipschitz constant
    L = 100  # Known Lipschitz constant
    assert abs(u2 - u1) <= L * abs(perturbation), \
        f"Discontinuity detected: Δu={u2-u1}, Δx={perturbation}"