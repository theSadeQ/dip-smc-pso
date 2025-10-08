# Example from: docs\testing\validation_methodology_guide.md
# Index: 11
# Runnable: True
# Hash: 2befa3c6

class TestPhysicsParameterValidation:
    """Validate physics parameter constraints."""

    def test_positive_mass_requirement(self):
        """Test all masses must be positive."""
        from src.core.dynamics import SimplifiedDynamics

        valid_config = {
            'M': 1.0, 'm1': 0.1, 'm2': 0.1,
            'L1': 0.5, 'L2': 0.5, 'g': 9.81
        }

        dynamics = SimplifiedDynamics(valid_config)
        assert dynamics.M == 1.0

        # Invalid: negative mass
        invalid_config = valid_config.copy()
        invalid_config['M'] = -1.0

        with pytest.raises(ValueError, match="Mass must be positive"):
            SimplifiedDynamics(invalid_config)

    def test_positive_length_requirement(self):
        """Test pendulum lengths must be positive."""
        from src.core.dynamics import SimplifiedDynamics

        valid_config = {
            'M': 1.0, 'm1': 0.1, 'm2': 0.1,
            'L1': 0.5, 'L2': 0.5, 'g': 9.81
        }

        # Invalid: zero length
        invalid_config = valid_config.copy()
        invalid_config['L1'] = 0.0

        with pytest.raises(ValueError, match="Length must be positive"):
            SimplifiedDynamics(invalid_config)