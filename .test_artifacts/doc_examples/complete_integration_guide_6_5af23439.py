# Example from: docs\workflows\complete_integration_guide.md
# Index: 6
# Runnable: True
# Hash: 5af23439

# Multi-objective optimization for competing requirements
from src.optimizer.multi_objective_pso import MultiObjectivePSOTuner

def multi_objective_optimization():
    """Optimize for multiple competing objectives."""

    objectives = {
        'tracking_performance': 0.4,  # Weight: 40%
        'control_effort': 0.3,        # Weight: 30%
        'robustness': 0.3             # Weight: 30%
    }

    tuner = MultiObjectivePSOTuner(
        bounds=get_pso_bounds('hybrid_adaptive_sta_smc'),
        objectives=objectives,
        n_particles=30,
        iters=300
    )

    pareto_front = tuner.optimize_pareto_front()
    return pareto_front