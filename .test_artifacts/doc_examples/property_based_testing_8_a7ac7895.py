# Example from: docs\testing\guides\property_based_testing.md
# Index: 8
# Runnable: False
# Hash: a7ac7895

# example-metadata:
# runnable: false

def positive_gains(min_value=0.1, max_value=100):
    """Generate valid controller gains"""
    return st.floats(
        min_value=min_value,
        max_value=max_value,
        allow_nan=False,
        allow_infinity=False,
        exclude_min=True  # Must be strictly positive
    )

@given(
    k1=positive_gains(),
    k2=positive_gains(),
    k3=positive_gains()
)
def test_smc_with_random_gains(k1, k2, k3):
    """SMC must remain stable for any positive gains"""
    controller = ClassicalSMC(gains=[k1, k2, k3])
    # Test stability property
    ...