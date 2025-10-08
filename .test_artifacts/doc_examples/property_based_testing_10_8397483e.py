# Example from: docs\testing\guides\property_based_testing.md
# Index: 10
# Runnable: True
# Hash: 8397483e

from hypothesis import given, assume, settings
import hypothesis.strategies as st

@given(state=valid_states())
@settings(max_examples=1000)  # Run 1000 random tests
def test_invariant_holds(state):
    """Template for testing control invariants"""
    # Optionally filter invalid cases
    assume(is_physically_realizable(state))

    # Compute control
    u = controller.compute_control(state)

    # Check invariant
    assert invariant_check(u, state), \
        f"Invariant violated for state={state}, control={u}"