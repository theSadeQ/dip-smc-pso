# Example from: docs\testing\guides\property_based_testing.md
# Index: 15
# Runnable: False
# Hash: 546d05ff

# example-metadata:
# runnable: false

@given(state=valid_states())
def test_property(state):
    # Filter out uninteresting cases
    assume(np.linalg.norm(state) > 0.01)  # Skip near-equilibrium
    ...