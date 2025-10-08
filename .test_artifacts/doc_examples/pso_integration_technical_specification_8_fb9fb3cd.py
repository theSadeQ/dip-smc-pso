# Example from: docs\pso_integration_technical_specification.md
# Index: 8
# Runnable: False
# Hash: fb9fb3cd

# example-metadata:
# runnable: false

def robust_optimization_under_uncertainty(pso_tuner: PSOTuner,
                                        uncertainty_config: PhysicsUncertaintySchema) -> dict:
    """
    Monte Carlo robust optimization with uncertainty quantification.

    Methodology:
    1. Sample N physics realizations from uncertainty distributions
    2. Evaluate each particle against all realizations
    3. Aggregate costs using risk-sensitive criteria (mean + α·std)
    4. Report confidence intervals for optimal gains

    Mathematical Framework:
    - Uncertain parameters: θ ~ N(θ₀, σ²) for each physics parameter
    - Robust cost: J_robust = E[J(G,θ)] + α·Std[J(G,θ)]
    - Risk parameter: α ∈ [0, 1] balancing mean vs variance
    """
    # Generate uncertainty samples
    physics_samples = generate_physics_samples(uncertainty_config)

    # Multi-realization evaluation
    costs_per_realization = []
    for physics_params in physics_samples:
        # Evaluate swarm under this realization
        realization_costs = pso_tuner.evaluate_swarm_with_physics(physics_params)
        costs_per_realization.append(realization_costs)

    # Risk-sensitive aggregation
    mean_costs = np.mean(costs_per_realization, axis=0)
    std_costs = np.std(costs_per_realization, axis=0)
    robust_costs = mean_costs + uncertainty_config.risk_factor * std_costs

    return {
        'robust_costs': robust_costs,
        'mean_costs': mean_costs,
        'std_costs': std_costs,
        'confidence_intervals': compute_confidence_intervals(costs_per_realization),
        'physics_samples': physics_samples
    }