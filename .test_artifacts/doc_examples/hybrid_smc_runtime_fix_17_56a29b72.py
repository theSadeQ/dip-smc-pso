# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 17
# Runnable: True
# Hash: 56a29b72

# tests/test_controllers/test_return_types.py
import pytest
import numpy as np
from src.controllers.smc.hybrid_adaptive_sta_smc import HybridAdaptiveSTASMC

class TestReturnTypes:
    """Comprehensive return type validation tests."""

    def test_compute_control_return_type(self):
        """Verify compute_control returns HybridSTAOutput."""
        controller = HybridAdaptiveSTASMC(
            gains=[10, 5, 8, 3],
            dt=0.01,
            max_force=100.0,
            k1_init=2.0,
            k2_init=1.0,
            gamma1=0.5,
            gamma2=0.3,
            dead_zone=0.01
        )

        state = np.zeros(6)
        state_vars = controller.initialize_state()
        history = controller.initialize_history()

        result = controller.compute_control(state, state_vars, history)

        # Type assertions
        assert isinstance(result, HybridSTAOutput)
        assert hasattr(result, 'control')
        assert hasattr(result, 'state_vars')
        assert hasattr(result, 'history')
        assert hasattr(result, 'sliding_surface')

    def test_compute_control_never_returns_none(self):
        """Ensure compute_control never returns None."""
        controller = HybridAdaptiveSTASMC(gains=[10, 5, 8, 3])

        # Test with various states including edge cases
        test_states = [
            np.zeros(6),                    # Zero state
            np.ones(6) * 0.1,              # Small values
            np.array([1, 0.5, -0.3, 0.1, -0.2, 0.05]),  # Mixed values
            np.array([0, 3.14, -3.14, 0, 0, 0]),        # Large angles
        ]

        for state in test_states:
            result = controller.compute_control(state)
            assert result is not None, f"compute_control returned None for state {state}"

    def test_reset_return_type(self):
        """Verify reset method returns None (as intended)."""
        controller = HybridAdaptiveSTASMC(gains=[10, 5, 8, 3])
        result = controller.reset()
        assert result is None, "reset() should return None"