# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 18
# Runnable: True
# Hash: 9fd60b0e

class TestPSOIntegration:
    """Integration tests for PSO optimization workflows."""

    def test_pso_optimization_workflow(self):
        """Test complete PSO optimization workflow."""
        from src.optimizer.pso_optimizer import PSOTuner

        bounds = [(0.1, 50.0)] * 4 + [(1.0, 200.0), (0.0, 50.0)]

        tuner = PSOTuner(
            controller_type='classical_smc',
            bounds=bounds,
            n_particles=10,
            iters=5
        )

        best_gains, best_cost = tuner.optimize()

        # Validate optimization results
        assert len(best_gains) == 6
        assert all(bounds[i][0] <= best_gains[i] <= bounds[i][1] for i in range(6))
        assert best_cost < float('inf')
        assert not np.isnan(best_cost)

    def test_optimized_gains_improve_performance(self):
        """Test that PSO-optimized gains improve performance."""
        from src.optimizer.pso_optimizer import PSOTuner
        from src.controllers.smc.classic_smc import ClassicalSMC
        from src.core.simulation_runner import run_simulation

        # Initial (unoptimized) gains
        initial_gains = [5.0, 5.0, 10.0, 10.0, 30.0, 2.0]

        # Run PSO optimization
        bounds = [(0.1, 50.0)] * 4 + [(1.0, 200.0), (0.0, 50.0)]
        tuner = PSOTuner(
            controller_type='classical_smc',
            bounds=bounds,
            n_particles=10,
            iters=10
        )
        optimized_gains, _ = tuner.optimize()

        # Compare performance
        def evaluate_performance(gains):
            controller = ClassicalSMC(gains=gains, max_force=100.0, boundary_layer=0.01)
            result = run_simulation(
                controller=controller,
                duration=5.0,
                dt=0.01,
                initial_state=[0.0, 0.0, 0.1, 0.1, 0.0, 0.0]
            )
            # ISE metric
            states = np.array(result['states'])
            return np.sum(np.sum(states**2, axis=1) * 0.01)

        initial_ise = evaluate_performance(initial_gains)
        optimized_ise = evaluate_performance(optimized_gains)

        # PSO should improve (reduce) ISE
        assert optimized_ise < initial_ise