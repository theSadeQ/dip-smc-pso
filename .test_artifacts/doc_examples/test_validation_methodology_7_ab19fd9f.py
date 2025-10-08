# Example from: docs\mathematical_foundations\test_validation_methodology.md
# Index: 7
# Runnable: False
# Hash: ab19fd9f

# example-metadata:
# runnable: false

class TestClassicalSMCConfigValidation:
    """Test configuration parameter validation."""

    def test_positive_gain_requirement(self):
        """Test that all surface gains must be positive."""
        # Valid configuration
        valid_gains = [5.0, 3.0, 4.0, 2.0, 10.0, 1.0]
        config = ClassicalSMCConfig(gains=valid_gains, max_force=100, dt=0.01, boundary_layer=0.01)

        # Invalid: zero gain
        with pytest.raises(ValueError, match="must be positive"):
            invalid_gains = [0.0, 3.0, 4.0, 2.0, 10.0, 1.0]
            ClassicalSMCConfig(gains=invalid_gains, max_force=100, dt=0.01, boundary_layer=0.01)

        # Invalid: negative gain
        with pytest.raises(ValueError, match="must be positive"):
            invalid_gains = [5.0, -3.0, 4.0, 2.0, 10.0, 1.0]
            ClassicalSMCConfig(gains=invalid_gains, max_force=100, dt=0.01, boundary_layer=0.01)

    def test_switching_gain_validation(self):
        """Test switching gain must be positive."""
        with pytest.raises(ValueError, match="Switching gain K must be positive"):
            invalid_gains = [5.0, 3.0, 4.0, 2.0, -10.0, 1.0]  # K < 0
            ClassicalSMCConfig(gains=invalid_gains, max_force=100, dt=0.01, boundary_layer=0.01)

    def test_boundary_layer_validation(self):
        """Test boundary layer thickness validation."""
        # Valid boundary layer
        valid_gains = [5.0, 3.0, 4.0, 2.0, 10.0, 1.0]
        config = ClassicalSMCConfig(gains=valid_gains, max_force=100, dt=0.01, boundary_layer=0.05)

        # Invalid: zero boundary layer
        with pytest.raises(ValueError, match="boundary_layer must be positive"):
            ClassicalSMCConfig(gains=valid_gains, max_force=100, dt=0.01, boundary_layer=0.0)

        # Invalid: negative boundary layer
        with pytest.raises(ValueError, match="boundary_layer must be positive"):
            ClassicalSMCConfig(gains=valid_gains, max_force=100, dt=0.01, boundary_layer=-0.01)