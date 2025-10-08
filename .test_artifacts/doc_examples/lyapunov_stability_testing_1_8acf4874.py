# Example from: docs\testing\theory\lyapunov_stability_testing.md
# Index: 1
# Runnable: True
# Hash: 8acf4874

import pytest
import numpy as np
from hypothesis import given, strategies as st

@given(state=valid_states())
def test_lyapunov_positive_definite(state):
    """V(x) ≥ 0 for all x, V(0) = 0"""
    V = lyapunov_function(state)

    if np.allclose(state, 0, atol=1e-6):
        assert V < 1e-6, f"V(0) = {V} ≠ 0"
    else:
        assert V > 0, f"V not positive: V({state}) = {V}"