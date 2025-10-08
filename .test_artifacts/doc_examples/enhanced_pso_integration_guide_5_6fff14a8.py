# Example from: docs\factory\enhanced_pso_integration_guide.md
# Index: 5
# Runnable: False
# Hash: 6fff14a8

def adaptive_pso_optimization(
    controller_type: str,
    simulation_config: Any,
    adaptation_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Adaptive PSO with dynamic parameter adjustment.

    Features:
    - Dynamic PSO parameter adjustment based on convergence
    - Adaptive bounds tightening around promising regions
    - Early stopping with convergence detection
    - Exploration-exploitation balance optimization
    """

    # Initialize adaptive PSO
    adaptive_pso = AdaptivePSOOptimizer(
        controller_type=controller_type,
        config=adaptation_config
    )

    # Multi-stage optimization
    stages = [
        {'exploration_weight': 0.8, 'iterations': 50},   # Exploration phase
        {'exploration_weight': 0.5, 'iterations': 30},   # Balanced phase
        {'exploration_weight': 0.2, 'iterations': 20}    # Exploitation phase
    ]

    all_results = []

    for stage_idx, stage_config in enumerate(stages):
        print(f"PSO Stage {stage_idx + 1}: {stage_config}")

        # Adjust PSO parameters
        adaptive_pso.update_parameters(stage_config)

        # Run optimization stage
        stage_result = adaptive_pso.optimize_stage(
            simulation_config, stage_config['iterations']
        )

        all_results.append(stage_result)

        # Check for early convergence
        if adaptive_pso.check_convergence():
            print(f"Converged early at stage {stage_idx + 1}")
            break

    # Combine results
    final_result = adaptive_pso.combine_stage_results(all_results)

    return final_result