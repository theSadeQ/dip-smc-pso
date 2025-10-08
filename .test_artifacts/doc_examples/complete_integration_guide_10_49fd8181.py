# Example from: docs\workflows\complete_integration_guide.md
# Index: 10
# Runnable: True
# Hash: 49fd8181

# Statistical hypothesis testing for controller comparison
from scipy import stats
import numpy as np

def hypothesis_testing_analysis():
    """Perform hypothesis testing for controller superiority."""

    # Null hypothesis: No significant difference between controllers
    # Alternative: Hybrid SMC performs significantly better

    controllers = ['classical_smc', 'adaptive_smc', 'sta_smc', 'hybrid_adaptive_sta_smc']
    performance_data = collect_performance_data(controllers, n_runs=50)

    # Perform pairwise t-tests
    test_results = {}

    for i, controller_a in enumerate(controllers):
        for j, controller_b in enumerate(controllers[i+1:], i+1):
            # Two-sample t-test
            t_stat, p_value = stats.ttest_ind(
                performance_data[controller_a]['settling_time'],
                performance_data[controller_b]['settling_time'],
                equal_var=False  # Welch's t-test
            )

            test_results[f"{controller_a}_vs_{controller_b}"] = {
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < 0.05,
                'effect_size': cohen_d(
                    performance_data[controller_a]['settling_time'],
                    performance_data[controller_b]['settling_time']
                )
            }

    return test_results