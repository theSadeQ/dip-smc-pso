# Example from: docs\technical\pso_integration_workflows.md
# Index: 23
# Runnable: False
# Hash: 8714d2f1

# example-metadata:
# runnable: false

# Guidelines for population size selection:
population_guidelines = {
    'small_problems': {
        'gains_count': '≤ 4',
        'recommended_size': '15-20',
        'reasoning': 'Sufficient diversity for low-dimensional search'
    },
    'medium_problems': {
        'gains_count': '5-6',
        'recommended_size': '20-30',
        'reasoning': 'Balanced exploration/exploitation'
    },
    'large_problems': {
        'gains_count': '> 6',
        'recommended_size': '30-50',
        'reasoning': 'Increased diversity for complex landscapes'
    }
}

def get_recommended_population_size(controller_type: ControllerType) -> int:
    """Get recommended population size for controller type."""

    gain_counts = {
        ControllerType.CLASSICAL_SMC: 6,
        ControllerType.STA_SMC: 6,
        ControllerType.ADAPTIVE_SMC: 5,
        ControllerType.HYBRID_SMC: 4
    }

    n_gains = gain_counts.get(controller_type, 6)

    if n_gains <= 4:
        return 20
    elif n_gains <= 6:
        return 25
    else:
        return 35