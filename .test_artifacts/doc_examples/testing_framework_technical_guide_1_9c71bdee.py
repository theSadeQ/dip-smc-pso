# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 1
# Runnable: True
# Hash: 9c71bdee

# tests/test_controllers/smc/algorithms/classical/test_classical_smc.py
import pytest
import numpy as np
from src.controllers.smc.classic_smc import ClassicalSMC

class TestClassicalSMC:
    """Unit tests for Classical Sliding Mode Controller."""

    def test_initialization_valid_parameters(self):
        """Test controller initialization with valid parameters."""
        gains = [10.0, 8.0, 15.0, 12.0, 50.0, 5.0]
        controller = ClassicalSMC(
            gains=gains,
            max_force=100.0,
            boundary_layer=0.01,
            dt=0.01
        )

        assert controller.k1 == 10.0
        assert controller.k2 == 8.0
        assert controller.lam1 == 15.0
        assert controller.lam2 == 12.0
        assert controller.K == 50.0
        assert controller.kd == 5.0
        assert controller.max_force == 100.0
        assert controller.boundary_layer == 0.01

    def test_compute_control_valid_output(self):
        """Test that compute_control returns finite, bounded output."""
        gains = [10.0, 8.0, 15.0, 12.0, 50.0, 5.0]
        controller = ClassicalSMC(gains=gains, max_force=100.0, boundary_layer=0.01)

        state = np.array([0.1, 0.05, 0.08, 0.02, 0.03, 0.01])
        result = controller.compute_control(state, {}, {})

        control = result.get('control_output', result.get('control', result.get('u')))
        assert control is not None
        assert np.all(np.isfinite(control))
        assert np.all(np.abs(control) <= 100.0)  # Within saturation

    def test_gain_validation(self):
        """Test that invalid gains are rejected."""
        # Negative gain should raise ValueError
        with pytest.raises(ValueError, match="must be positive"):
            ClassicalSMC(
                gains=[10.0, -8.0, 15.0, 12.0, 50.0, 5.0],
                max_force=100.0,
                boundary_layer=0.01
            )

        # Zero gain should raise ValueError
        with pytest.raises(ValueError, match="must be positive"):
            ClassicalSMC(
                gains=[0.0, 8.0, 15.0, 12.0, 50.0, 5.0],
                max_force=100.0,
                boundary_layer=0.01
            )