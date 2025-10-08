# Example from: docs\mathematical_foundations\algorithm_fixes_summary.md
# Index: 9
# Runnable: False
# Hash: 1cf9f2ec

class TestConfigurationValidationCoverage:
       """Comprehensive coverage of all validation rules."""

       @pytest.mark.parametrize("invalid_gain_index", [0, 1, 2, 3])
       def test_zero_surface_gains_rejection(self, invalid_gain_index):
           """Test rejection of zero surface gains."""
           gains = [5.0, 3.0, 4.0, 2.0, 10.0, 1.0]
           gains[invalid_gain_index] = 0.0

           with pytest.raises(ValueError, match="must be positive"):
               ClassicalSMCConfig(gains=gains, max_force=100, dt=0.01, boundary_layer=0.01)

       @pytest.mark.parametrize("invalid_gain_index", [0, 1, 2, 3])
       def test_negative_surface_gains_rejection(self, invalid_gain_index):
           """Test rejection of negative surface gains."""
           gains = [5.0, 3.0, 4.0, 2.0, 10.0, 1.0]
           gains[invalid_gain_index] = -1.0

           with pytest.raises(ValueError, match="must be positive"):
               ClassicalSMCConfig(gains=gains, max_force=100, dt=0.01, boundary_layer=0.01)