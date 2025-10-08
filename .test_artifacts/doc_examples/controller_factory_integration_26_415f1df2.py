# Example from: docs\technical\controller_factory_integration.md
# Index: 26
# Runnable: True
# Hash: 415f1df2

def test_performance_significance(results_A, results_B, metric='settling_time'):
    """Test statistical significance of performance differences."""

    from scipy import stats

    data_A = results_A[metric]['samples']
    data_B = results_B[metric]['samples']

    # Perform Welch's t-test (unequal variances)
    t_stat, p_value = stats.ttest_ind(data_A, data_B, equal_var=False)

    # Compute effect size (Cohen's d)
    pooled_std = np.sqrt((np.var(data_A) + np.var(data_B)) / 2)
    cohens_d = (np.mean(data_A) - np.mean(data_B)) / pooled_std

    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'effect_size': cohens_d,
        'significant': p_value < 0.05
    }