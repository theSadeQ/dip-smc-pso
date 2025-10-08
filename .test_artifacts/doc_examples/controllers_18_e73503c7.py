# Example from: docs\guides\api\controllers.md
# Index: 18
# Runnable: True
# Hash: e73503c7

# tests/test_controllers/test_terminal_smc.py
import pytest
import numpy as np
from my_custom_controller import TerminalSMC

def test_initialization():
    """Test controller initializes correctly."""
    controller = TerminalSMC(gains=[10, 8, 15, 12, 50, 5, 7])
    assert controller.K == 50.0
    assert controller.p == 5.0
    assert controller.q == 7.0

def test_compute_control():
    """Test control computation."""
    controller = TerminalSMC(gains=[10, 8, 15, 12, 50, 5, 7])
    state = np.array([0, 0, 0.1, 0, 0.15, 0])

    control, state_vars, history = controller.compute_control(
        state, {}, controller.initialize_history()
    )

    assert isinstance(control, (float, np.floating))
    assert abs(control) <= 100.0  # Saturation check

def test_saturation():
    """Test control saturates at max_force."""
    controller = TerminalSMC(gains=[10, 8, 15, 12, 500, 5, 7], max_force=100.0)
    state = np.array([0, 0, 0.5, 0, 0.6, 0])  # Large errors

    control, _, _ = controller.compute_control(state, {}, controller.initialize_history())

    assert abs(control) == 100.0