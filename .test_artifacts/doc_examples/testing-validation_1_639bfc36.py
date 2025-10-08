# Example from: docs\guides\how-to\testing-validation.md
# Index: 1
# Runnable: True
# Hash: 639bfc36

# tests/test_controllers/test_my_controller.py
import pytest
import numpy as np
from src.controllers.my_controller import MyController


class TestMyController:
    """Unit tests for MyController."""

    def test_initialization(self):
        """Test controller initializes correctly."""
        gains = [10.0, 8.0, 15.0, 12.0, 50.0, 5.0]
        controller = MyController(gains=gains, max_force=100.0)

        assert controller.gains == gains
        assert controller.max_force == 100.0

    def test_invalid_gain_count(self):
        """Test ValueError raised for wrong number of gains."""
        gains = [10.0, 8.0]  # Too few
        with pytest.raises(ValueError, match="6 gains"):
            MyController(gains=gains, max_force=100.0)

    def test_compute_control(self):
        """Test control computation."""
        controller = MyController(
            gains=[10, 8, 15, 12, 50, 5],
            max_force=100.0
        )

        state = np.array([0, 0, 0.1, 0, 0.15, 0])
        control, state_vars, history = controller.compute_control(
            state, {}, {}
        )

        # Check control is computed
        assert isinstance(control, (float, np.floating))

        # Check bounds
        assert abs(control) <= 100.0

    def test_control_saturation(self):
        """Test control saturates at max_force."""
        controller = MyController(
            gains=[10, 8, 15, 12, 500.0, 5.0],  # Very high K
            max_force=100.0
        )

        state = np.array([0, 0, 0.5, 0, 0.6, 0])  # Large errors
        control, _, _ = controller.compute_control(state, {}, {})

        assert abs(control) == 100.0  # Should saturate

    def test_equilibrium(self):
        """Test zero control at equilibrium."""
        controller = MyController(
            gains=[10, 8, 15, 12, 50, 5],
            max_force=100.0
        )

        state = np.zeros(6)  # Perfect equilibrium
        control, _, _ = controller.compute_control(state, {}, {})

        assert abs(control) < 1e-6  # Nearly zero