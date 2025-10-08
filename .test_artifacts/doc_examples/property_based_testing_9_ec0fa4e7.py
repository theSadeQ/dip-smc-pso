# Example from: docs\testing\guides\property_based_testing.md
# Index: 9
# Runnable: True
# Hash: ec0fa4e7

def trajectories(duration=5.0, dt=0.01):
    """Generate state trajectories"""
    return st.lists(
        valid_states(),
        min_size=int(duration / dt),
        max_size=int(duration / dt)
    )