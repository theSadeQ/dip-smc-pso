# Example from: docs\guides\tutorials\tutorial-04-custom-controller.md
# Index: 5
# Runnable: True
# Hash: 340d92e6

import pytest
import numpy as np
from src.controllers.smc.terminal_smc import TerminalSMC


class TestTerminalSMC:
    """Unit tests for Terminal SMC controller."""

    def test_initialization_valid_gains(self):
        """Test controller initializes with valid gains."""
        gains = [10.0, 8.0, 15.0, 12.0, 50.0, 0.5, 0.7]
        controller = TerminalSMC(gains=gains, max_force=100.0, boundary_layer=0.01)

        assert controller.k1 == 10.0
        assert controller.alpha == 0.5
        assert controller.beta == 0.7

    def test_initialization_invalid_gain_count(self):
        """Test ValueError raised for wrong number of gains."""
        gains = [10.0, 8.0, 15.0]  # Only 3 gains
        with pytest.raises(ValueError, match="7 gains"):
            TerminalSMC(gains=gains, max_force=100.0, boundary_layer=0.01)

    def test_initialization_invalid_exponents(self):
        """Test ValueError for invalid terminal exponents."""
        gains = [10.0, 8.0, 15.0, 12.0, 50.0, 1.5, 0.7]  # α > 1
        with pytest.raises(ValueError, match="must be in"):
            TerminalSMC(gains=gains, max_force=100.0, boundary_layer=0.01)

    def test_sliding_surface_computation(self):
        """Test sliding surface calculation."""
        gains = [10.0, 8.0, 15.0, 12.0, 50.0, 0.5, 0.7]
        controller = TerminalSMC(gains=gains, max_force=100.0, boundary_layer=0.01)

        state = np.array([0.0, 0.0, 0.1, 0.0, 0.15, 0.0])
        s = controller.compute_sliding_surface(state)

        # s = k1·θ1 + k2·0 + λ1·θ2 + λ2·0 = 10*0.1 + 15*0.15 = 3.25
        assert abs(s - 3.25) < 0.01

    def test_control_computation(self):
        """Test control signal computation."""
        gains = [10.0, 8.0, 15.0, 12.0, 50.0, 0.5, 0.7]
        controller = TerminalSMC(gains=gains, max_force=100.0, boundary_layer=0.01)

        state = np.array([0.0, 0.0, 0.1, 0.0, 0.15, 0.0])
        control, state_vars, history = controller.compute_control(state, {}, {})

        # Control should be computed and bounded
        assert isinstance(control, (float, np.floating))
        assert abs(control) <= 100.0  # max_force

    def test_control_saturation(self):
        """Test control saturation at max_force."""
        gains = [10.0, 8.0, 15.0, 12.0, 500.0, 0.5, 0.7]  # Very high K
        controller = TerminalSMC(gains=gains, max_force=100.0, boundary_layer=0.01)

        state = np.array([0.0, 0.0, 0.5, 0.0, 0.6, 0.0])  # Large errors
        control, _, _ = controller.compute_control(state, {}, {})

        # Control should saturate at max_force
        assert abs(control) == 100.0

    def test_cleanup(self):
        """Test resource cleanup."""
        gains = [10.0, 8.0, 15.0, 12.0, 50.0, 0.5, 0.7]
        controller = TerminalSMC(gains=gains, max_force=100.0, boundary_layer=0.01)
        controller.cleanup()

        # Dynamics reference should be None after cleanup
        assert controller._dynamics_ref is None