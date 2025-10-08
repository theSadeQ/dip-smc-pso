# Example from: docs\testing\guides\property_based_testing.md
# Index: 17
# Runnable: False
# Hash: e79b8150

from hypothesis import settings, HealthCheck

@given(state=valid_states())
@settings(
    max_examples=10000,  # Exhaustive testing
    deadline=None,       # No timeout
    suppress_health_check=[HealthCheck.too_slow]
)
def test_critical_property(state):
    ...