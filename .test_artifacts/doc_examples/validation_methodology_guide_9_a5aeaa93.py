# Example from: docs\testing\validation_methodology_guide.md
# Index: 9
# Runnable: True
# Hash: a5aeaa93

# tests/validation/test_configuration_validation.py

class TestControllerGainValidation:
    """Validate controller gain configuration rules."""

    def test_positive_gain_requirement(self):
        """Test that all gains must be positive."""
        from src.controllers.smc.classic_smc import ClassicalSMC

        # Valid gains
        valid_gains = [10.0, 8.0, 15.0, 12.0, 50.0, 5.0]
        controller = ClassicalSMC(gains=valid_gains, max_force=100.0)
        assert controller.k1 == 10.0

        # Invalid: negative gain
        with pytest.raises(ValueError, match="must be positive"):
            ClassicalSMC(
                gains=[10.0, -8.0, 15.0, 12.0, 50.0, 5.0],
                max_force=100.0
            )

        # Invalid: zero gain
        with pytest.raises(ValueError, match="must be positive"):
            ClassicalSMC(
                gains=[0.0, 8.0, 15.0, 12.0, 50.0, 5.0],
                max_force=100.0
            )

    def test_switching_gain_validation(self):
        """Test switching gain K must be positive."""
        from src.controllers.smc.classic_smc import ClassicalSMC

        with pytest.raises(ValueError, match="Switching gain K must be positive"):
            ClassicalSMC(
                gains=[10.0, 8.0, 15.0, 12.0, -50.0, 5.0],  # Negative K
                max_force=100.0
            )

    def test_boundary_layer_validation(self):
        """Test boundary layer thickness must be positive."""
        from src.controllers.smc.classic_smc import ClassicalSMC

        valid_gains = [10.0, 8.0, 15.0, 12.0, 50.0, 5.0]

        # Valid boundary layer
        controller = ClassicalSMC(gains=valid_gains, max_force=100.0, boundary_layer=0.01)
        assert controller.boundary_layer == 0.01

        # Invalid: zero boundary layer
        with pytest.raises(ValueError, match="boundary_layer must be positive"):
            ClassicalSMC(gains=valid_gains, max_force=100.0, boundary_layer=0.0)

        # Invalid: negative boundary layer
        with pytest.raises(ValueError, match="boundary_layer must be positive"):
            ClassicalSMC(gains=valid_gains, max_force=100.0, boundary_layer=-0.01)