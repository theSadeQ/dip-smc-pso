# Example from: docs\workflows\complete_integration_guide.md
# Index: 19
# Runnable: True
# Hash: ec58caa8

# Comprehensive testing for new controllers
import pytest
from hypothesis import given, strategies as st

class TestNewController:
    """Comprehensive test suite for new controller."""

    def test_controller_initialization(self):
        """Test controller initialization."""
        controller = NewControllerTemplate(
            gains=[1.0, 2.0, 3.0, 4.0],
            dt=0.01,
            max_force=100.0
        )
        assert controller.n_gains == 4
        assert controller.gains == [1.0, 2.0, 3.0, 4.0]

    @given(st.lists(st.floats(min_value=-10, max_value=10), min_size=6, max_size=6))
    def test_control_computation_stability(self, state_values):
        """Test control computation with random states."""
        controller = NewControllerTemplate(gains=[1, 2, 3, 4])
        state = np.array(state_values)

        result = controller.compute_control(state)

        # Basic stability checks
        assert result is not None
        assert np.isfinite(result.control)
        assert abs(result.control) <= controller.max_force

    def test_pso_integration(self):
        """Test PSO optimization integration."""
        from src.optimizer.pso_optimizer import PSOTuner

        bounds = [(0.1, 10.0)] * 4  # Bounds for 4 gains
        tuner = PSOTuner(bounds=bounds, n_particles=10, iters=20)

        best_gains, best_cost = tuner.optimize(
            controller_type='new_controller_template',
            dynamics=test_dynamics
        )

        assert len(best_gains) == 4
        assert best_cost >= 0.0