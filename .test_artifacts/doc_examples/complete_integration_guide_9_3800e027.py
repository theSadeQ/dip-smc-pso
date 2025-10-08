# Example from: docs\workflows\complete_integration_guide.md
# Index: 9
# Runnable: False
# Hash: 3800e027

# example-metadata:
# runnable: false

# Statistical validation of controller performance
from src.utils.statistics import MonteCarloAnalyzer

def statistical_performance_analysis():
    """Perform statistical analysis of controller performance."""

    analyzer = MonteCarloAnalyzer(n_runs=100)

    controllers = ['classical_smc', 'adaptive_smc', 'sta_smc', 'hybrid_adaptive_sta_smc']
    statistics = {}

    for controller_type in controllers:
        print(f"📈 Analyzing {controller_type}...")

        # Run Monte Carlo analysis
        results = analyzer.analyze_controller(
            controller_type=controller_type,
            test_conditions={
                'initial_disturbance': 'random_uniform_0.1',
                'parameter_uncertainty': 0.1,
                'measurement_noise': 0.01
            }
        )

        statistics[controller_type] = {
            'settling_time': {
                'mean': results.settling_time.mean(),
                'std': results.settling_time.std(),
                'confidence_interval': results.settling_time_ci_95
            },
            'overshoot': {
                'mean': results.overshoot.mean(),
                'std': results.overshoot.std(),
                'confidence_interval': results.overshoot_ci_95
            },
            'control_effort': {
                'mean': results.control_effort.mean(),
                'std': results.control_effort.std(),
                'confidence_interval': results.control_effort_ci_95
            }
        }

    # Statistical comparison tests
    comparison_results = analyzer.statistical_comparison(statistics)

    return statistics, comparison_results