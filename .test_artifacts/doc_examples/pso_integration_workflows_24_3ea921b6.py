# Example from: docs\technical\pso_integration_workflows.md
# Index: 24
# Runnable: False
# Hash: 3ea921b6

def configure_convergence_criteria(controller_type: ControllerType,
                                 optimization_goal: str) -> PSOFactoryConfig:
    """Configure convergence criteria based on optimization goals."""

    criteria_map = {
        'fast_prototyping': {
            'max_iterations': 30,
            'convergence_threshold': 1e-4,
            'max_stagnation_iterations': 8
        },
        'research_quality': {
            'max_iterations': 75,
            'convergence_threshold': 1e-5,
            'max_stagnation_iterations': 12
        },
        'production_grade': {
            'max_iterations': 100,
            'convergence_threshold': 1e-6,
            'max_stagnation_iterations': 15
        }
    }

    criteria = criteria_map.get(optimization_goal, criteria_map['research_quality'])
    population_size = get_recommended_population_size(controller_type)

    return PSOFactoryConfig(
        controller_type=controller_type,
        population_size=population_size,
        **criteria,
        use_robust_evaluation=True,
        enable_adaptive_bounds=True
    )

# Usage examples
fast_config = configure_convergence_criteria(ControllerType.CLASSICAL_SMC, 'fast_prototyping')
research_config = configure_convergence_criteria(ControllerType.STA_SMC, 'research_quality')
production_config = configure_convergence_criteria(ControllerType.ADAPTIVE_SMC, 'production_grade')