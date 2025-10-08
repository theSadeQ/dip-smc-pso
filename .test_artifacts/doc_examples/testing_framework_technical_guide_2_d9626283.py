# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 2
# Runnable: True
# Hash: d9626283

# tests/integration/test_pso_controller_integration.py
import pytest
from src.controllers.factory import SMCFactory, SMCType
from src.optimizer.pso_optimizer import PSOTuner

class TestPSOControllerIntegration:
    """Integration tests for PSO optimization of SMC controllers."""

    def test_pso_optimization_classical_smc(self):
        """Test full PSO optimization pipeline for classical SMC."""
        # Setup
        bounds = [(0.1, 50.0)] * 4 + [(1.0, 200.0), (0.0, 50.0)]
        tuner = PSOTuner(
            controller_type='classical_smc',
            bounds=bounds,
            n_particles=10,
            iters=5  # Quick test
        )

        # Execute optimization
        best_gains, best_cost = tuner.optimize()

        # Validate results
        assert len(best_gains) == 6
        assert all(0.1 <= g <= 200.0 for g in best_gains)
        assert best_cost < float('inf')
        assert not np.isnan(best_cost)

    def test_optimized_controller_performance(self):
        """Test that PSO-optimized controller stabilizes system."""
        # Load PSO-optimized gains
        optimized_gains = [12.3, 9.1, 18.7, 14.2, 65.3, 7.8]

        controller = SMCFactory.create_controller(
            SMCType.CLASSICAL,
            gains=optimized_gains,
            max_force=100.0,
            boundary_layer=0.01
        )

        # Simulate
        from src.core.simulation_runner import run_simulation
        result = run_simulation(
            controller=controller,
            duration=5.0,
            dt=0.01,
            initial_state=[0.1, 0.1, 0.0, 0.0, 0.0, 0.0]
        )

        # Performance criteria
        final_state = result['states'][-1]
        assert np.linalg.norm(final_state) < 0.01  # Stabilized to equilibrium