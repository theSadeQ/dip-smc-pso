# Example from: docs\pso_optimization_workflow_user_guide.md
# Index: 13
# Runnable: True
# Hash: b5f916f6

def hybrid_pso_local_search(controller_factory, config):
    """Combine PSO global search with local refinement."""

    # Phase 1: Global PSO search
    pso_tuner = PSOTuner(controller_factory, config)
    pso_results = pso_tuner.optimize(
        bounds=bounds,
        n_particles=50,
        n_iterations=100
    )

    # Phase 2: Local refinement around best solution
    from scipy.optimize import minimize

    def local_objective(gains):
        controller = controller_factory(gains)
        # Simulate and return cost
        cost = simulate_and_evaluate(controller)
        return cost

    # Local optimization starting from PSO result
    local_result = minimize(
        local_objective,
        x0=pso_results['best_gains'],
        bounds=[(bounds[0][i], bounds[1][i]) for i in range(len(bounds[0]))],
        method='L-BFGS-B'
    )

    return {
        'pso_result': pso_results,
        'local_result': local_result,
        'final_gains': local_result.x,
        'final_cost': local_result.fun
    }