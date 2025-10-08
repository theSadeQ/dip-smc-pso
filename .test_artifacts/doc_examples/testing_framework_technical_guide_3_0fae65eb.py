# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 3
# Runnable: True
# Hash: 0fae65eb

# tests/test_controllers/smc/test_property_based_smc.py
from hypothesis import given, strategies as st
import numpy as np

class TestSlidingSurfaceProperties:
    """Property-based tests for sliding surface mathematics."""

    @given(
        k1=st.floats(min_value=0.1, max_value=50.0),
        k2=st.floats(min_value=0.1, max_value=50.0),
        lam1=st.floats(min_value=0.1, max_value=50.0),
        lam2=st.floats(min_value=0.1, max_value=50.0)
    )
    def test_sliding_surface_linearity(self, k1, k2, lam1, lam2):
        """Test linearity property: s(x1 + x2) = s(x1) + s(x2)."""
        gains = [k1, k2, lam1, lam2]
        surface = LinearSlidingSurface(gains)

        x1 = np.random.uniform(-1, 1, size=6)
        x2 = np.random.uniform(-1, 1, size=6)

        s1 = surface.compute(x1)
        s2 = surface.compute(x2)
        s_combined = surface.compute(x1 + x2)

        # Linearity property within numerical precision
        assert abs(s_combined - (s1 + s2)) < 1e-10

    @given(
        state=st.lists(
            st.floats(min_value=-10.0, max_value=10.0),
            min_size=6,
            max_size=6
        )
    )
    def test_controller_output_bounded(self, state):
        """Test that controller output is always bounded for finite input."""
        gains = [10.0, 8.0, 15.0, 12.0, 50.0, 5.0]
        controller = ClassicalSMC(gains=gains, max_force=100.0, boundary_layer=0.01)

        state_array = np.array(state)

        if np.all(np.isfinite(state_array)):
            result = controller.compute_control(state_array, {}, {})
            control = result.get('control_output', result.get('control'))

            if control is not None:
                # Control must be finite and within saturation limits
                assert np.all(np.isfinite(control))
                assert np.all(np.abs(control) <= 100.0)