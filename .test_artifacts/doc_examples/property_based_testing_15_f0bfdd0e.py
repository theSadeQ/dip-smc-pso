# Example from: docs\testing\guides\property_based_testing.md
# Index: 15
# Runnable: False
# Hash: f0bfdd0e

@given(state=valid_states())
def test_property(state):
    # Filter out uninteresting cases
    assume(np.linalg.norm(state) > 0.01)  # Skip near-equilibrium
    ...