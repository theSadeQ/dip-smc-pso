# Example from: docs\testing\guides\property_based_testing.md
# Index: 16
# Runnable: True
# Hash: 85137f74

@st.composite
def controller_with_valid_gains(draw):
    """Generate controller with constraint: k1 > k2 > k3"""
    k3 = draw(st.floats(min_value=1, max_value=10))
    k2 = draw(st.floats(min_value=k3 + 1, max_value=50))
    k1 = draw(st.floats(min_value=k2 + 1, max_value=100))
    return ClassicalSMC(gains=[k1, k2, k3])