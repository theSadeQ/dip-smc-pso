# Example from: docs\guides\how-to\optimization-workflows.md
# Index: 8
# Runnable: False
# Hash: 8afd3176

def multi_start_pso(n_restarts=3):
    """
    Run PSO multiple times with different initializations.
    """
    best_overall_cost = float('inf')
    best_overall_gains = None

    for restart in range(n_restarts):
        print(f"\nRestart {restart + 1}/{n_restarts}")

        # Different seed for each restart
        seed = 42 + restart * 100

        tuner = PSOTuner(
            controller_type='classical_smc',
            config=config,
            seed=seed
        )

        gains, cost = tuner.optimize()

        print(f"  Best cost: {cost:.4f}")

        if cost < best_overall_cost:
            best_overall_cost = cost
            best_overall_gains = gains

    print(f"\nBest across all restarts: {best_overall_cost:.4f}")
    return best_overall_gains, best_overall_cost