# Example from: docs\pso_factory_integration_patterns.md
# Index: 6
# Runnable: False
# Hash: e2a57e15

# example-metadata:
# runnable: false

def multi_stage_pso_optimization(controller_type: SMCType) -> Tuple[np.ndarray, float]:
    """Multi-stage PSO with progressive refinement."""

    # Stage 1: Coarse optimization with wide bounds
    logger.info("Stage 1: Coarse optimization")

    lower_bounds, upper_bounds = get_gain_bounds_for_pso(controller_type)

    # Expand bounds for exploration
    exploration_lower = [0.5 * lb for lb in lower_bounds]
    exploration_upper = [2.0 * ub for ub in upper_bounds]

    coarse_config = {
        'n_particles': 40,
        'max_iter': 50,
        'bounds': (exploration_lower, exploration_upper),
        'w': 0.9,  # High inertia for exploration
        'c1': 1.5,
        'c2': 1.5
    }

    coarse_factory = create_pso_controller_factory(controller_type)
    coarse_tuner = PSOTuner(
        controller_factory=lambda gains: evaluate_basic_performance(coarse_factory(gains)),
        config=config,
        **coarse_config
    )

    stage1_gains, stage1_fitness = coarse_tuner.optimize()

    # Stage 2: Fine optimization around best solution
    logger.info("Stage 2: Fine optimization")

    # Narrow bounds around stage 1 result
    bound_margin = 0.2  # 20% margin
    fine_lower = [max(lb, (1 - bound_margin) * g) for lb, g in zip(lower_bounds, stage1_gains)]
    fine_upper = [min(ub, (1 + bound_margin) * g) for ub, g in zip(upper_bounds, stage1_gains)]

    fine_config = {
        'n_particles': 30,
        'max_iter': 100,
        'bounds': (fine_lower, fine_upper),
        'w': 0.4,  # Low inertia for exploitation
        'c1': 2.0,
        'c2': 2.0
    }

    fine_factory = create_pso_controller_factory(controller_type)
    fine_tuner = PSOTuner(
        controller_factory=lambda gains: evaluate_detailed_performance(fine_factory(gains)),
        config=config,
        **fine_config
    )

    stage2_gains, stage2_fitness = fine_tuner.optimize()

    # Stage 3: Validation and robustness testing
    logger.info("Stage 3: Robustness validation")

    final_controller = fine_factory(stage2_gains)
    robustness_metrics = evaluate_robustness(final_controller)

    logger.info(f"Multi-stage optimization complete:")
    logger.info(f"Stage 1 (coarse): {stage1_fitness}")
    logger.info(f"Stage 2 (fine): {stage2_fitness}")
    logger.info(f"Final gains: {stage2_gains}")
    logger.info(f"Robustness score: {robustness_metrics['robustness_index']}")

    return stage2_gains, stage2_fitness