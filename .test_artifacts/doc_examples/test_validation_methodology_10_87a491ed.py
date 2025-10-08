# Example from: docs\mathematical_foundations\test_validation_methodology.md
# Index: 10
# Runnable: True
# Hash: 87a491ed

from hypothesis import given, strategies as st

class TestPropertyBasedSMC:
    """Property-based tests using Hypothesis."""

    @given(
        k1=st.floats(min_value=0.1, max_value=50.0),
        k2=st.floats(min_value=0.1, max_value=50.0),
        lam1=st.floats(min_value=0.1, max_value=50.0),
        lam2=st.floats(min_value=0.1, max_value=50.0),
        K=st.floats(min_value=1.0, max_value=200.0),
        kd=st.floats(min_value=0.0, max_value=20.0)
    )
    def test_configuration_property_all_positive_gains(self, k1, k2, lam1, lam2, K, kd):
        """Test that any positive gain combination creates valid configuration."""
        gains = [k1, k2, lam1, lam2, K, kd]

        # Should not raise any exceptions
        config = ClassicalSMCConfig(
            gains=gains,
            max_force=100.0,
            dt=0.01,
            boundary_layer=0.01
        )

        # All properties should be accessible
        assert config.k1 == k1
        assert config.k2 == k2
        assert config.lam1 == lam1
        assert config.lam2 == lam2
        assert config.K == K
        assert config.kd == kd

    @given(
        state=st.lists(
            st.floats(min_value=-10.0, max_value=10.0),
            min_size=6,
            max_size=6
        )
    )
    def test_sliding_surface_finite_output(self, state):
        """Test that sliding surface always produces finite output for finite input."""
        gains = [5.0, 3.0, 4.0, 2.0, 10.0, 1.0]
        surface = LinearSlidingSurface(gains[:4])

        state_array = np.array(state)

        # Sliding surface should always be finite for finite state
        if np.all(np.isfinite(state_array)):
            surface_value = surface.compute(state_array)
            assert np.isfinite(surface_value)

    @given(
        boundary_thickness=st.floats(min_value=1e-6, max_value=1.0),
        surface_value=st.floats(min_value=-100.0, max_value=100.0)
    )
    def test_boundary_layer_bounded_output(self, boundary_thickness, surface_value):
        """Test that boundary layer output is always bounded."""
        boundary_layer = BoundaryLayer(thickness=boundary_thickness, switch_method="tanh")

        if np.isfinite(surface_value):
            switch_value = boundary_layer.compute_switching_function(surface_value)

            # Switching function should be bounded between -1 and 1
            assert -1.0 <= switch_value <= 1.0
            assert np.isfinite(switch_value)