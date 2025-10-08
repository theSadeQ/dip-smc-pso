# Example from: docs\workflows\complete_integration_guide.md
# Index: 5
# Runnable: False
# Hash: 393c61c2

# scripts/custom_batch_optimization.py
from src.optimizer.pso_optimizer import PSOTuner
from src.controllers.factory import get_controller_types

def optimize_all_controllers():
    """Optimize all available controllers."""

    controllers = ['classical_smc', 'adaptive_smc', 'sta_smc', 'hybrid_adaptive_sta_smc']
    results = {}

    for controller_type in controllers:
        print(f"\n🚀 Optimizing {controller_type}...")

        # Get controller-specific PSO bounds
        bounds = get_pso_bounds(controller_type)

        # Create PSO tuner
        tuner = PSOTuner(
            bounds=bounds,
            n_particles=20,
            iters=200,
            options={'c1': 2.0, 'c2': 2.0, 'w': 0.7}
        )

        # Optimize
        best_gains, best_cost = tuner.optimize(
            controller_type=controller_type,
            dynamics=dynamics_model,
            seed=42
        )

        results[controller_type] = {
            'gains': best_gains,
            'cost': best_cost,
            'convergence': tuner.cost_history
        }

        print(f"✅ {controller_type}: Cost = {best_cost:.6f}")

    return results

if __name__ == "__main__":
    results = optimize_all_controllers()
    save_optimization_results(results, 'complete_optimization_results.json')