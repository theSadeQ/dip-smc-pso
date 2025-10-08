# Example from: docs\validation\validation_examples.md
# Index: 7
# Runnable: False
# Hash: 9cc5b582

"""
Statistical Comparison of Three SMC Variants
=============================================

This script performs rigorous statistical comparison of controller
performance using parametric and non-parametric tests with effect size analysis.
"""

import numpy as np
from src.analysis.validation.statistical_tests import StatisticalTestConfig, StatisticalTestSuite
from scipy import stats

# Random seed
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)


def simulate_controller_trials(controller_type: str, n_trials: int = 30) -> np.ndarray:
    """
    Simulate controller performance over multiple trials.

    Parameters
    ----------
    controller_type : str
        One of 'classical', 'super_twisting', 'adaptive'
    n_trials : int
        Number of trials to run

    Returns
    -------
    np.ndarray
        Settling times for each trial
    """
    # Simulate realistic settling times with different characteristics
    if controller_type == 'classical':
        # Classical SMC: moderate performance, moderate variance
        mean_settling = 2.5
        std_settling = 0.4
        settling_times = np.random.normal(mean_settling, std_settling, n_trials)

    elif controller_type == 'super_twisting':
        # Super-Twisting: best performance, low variance (finite-time convergence)
        mean_settling = 1.8
        std_settling = 0.25
        settling_times = np.random.normal(mean_settling, std_settling, n_trials)

    elif controller_type == 'adaptive':
        # Adaptive: good mean but higher variance (adaptation uncertainty)
        mean_settling = 2.1
        std_settling = 0.5
        settling_times = np.random.normal(mean_settling, std_settling, n_trials)
    else:
        raise ValueError(f"Unknown controller type: {controller_type}")

    # Ensure positive values
    settling_times = np.abs(settling_times)

    return settling_times


def compute_effect_size_cohens_d(group1: np.ndarray, group2: np.ndarray) -> dict:
    """
    Compute Cohen's d effect size.

    Returns
    -------
    dict
        Effect size, interpretation, and metadata
    """
    mean1 = np.mean(group1)
    mean2 = np.mean(group2)
    std1 = np.std(group1, ddof=1)
    std2 = np.std(group2, ddof=1)
    n1 = len(group1)
    n2 = len(group2)

    # Pooled standard deviation
    pooled_std = np.sqrt(((n1-1)*std1**2 + (n2-1)*std2**2) / (n1 + n2 - 2))

    # Cohen's d
    d = (mean1 - mean2) / pooled_std

    # Interpretation
    abs_d = abs(d)
    if abs_d < 0.2:
        interpretation = "negligible"
    elif abs_d < 0.5:
        interpretation = "small"
    elif abs_d < 0.8:
        interpretation = "medium"
    else:
        interpretation = "large"

    return {
        'd': d,
        'abs_d': abs_d,
        'interpretation': interpretation,
        'mean_diff': mean1 - mean2,
        'pooled_std': pooled_std
    }


def main():
    """Main statistical comparison script."""

    print("=" * 70)
    print("Statistical Comparison of Controller Performance")
    print("=" * 70)

    # Configuration
    n_trials = 30  # 30 trials per controller
    alpha = 0.05   # 5% significance level

    print(f"\n1. Experimental Setup:")
    print(f"   Controllers: Classical SMC, Super-Twisting SMC, Adaptive SMC")
    print(f"   Trials per controller: {n_trials}")
    print(f"   Significance level: {alpha}")
    print(f"   Metric: Settling time (seconds)")

    # Run simulations
    print(f"\n2. Collecting performance data...")

    classical_data = simulate_controller_trials('classical', n_trials)
    supertwisting_data = simulate_controller_trials('super_twisting', n_trials)
    adaptive_data = simulate_controller_trials('adaptive', n_trials)

    controllers = {
        'Classical SMC': classical_data,
        'Super-Twisting SMC': supertwisting_data,
        'Adaptive SMC': adaptive_data
    }

    # Descriptive statistics
    print(f"\n3. Descriptive Statistics:")
    print("-" * 70)

    for name, data in controllers.items():
        print(f"\n   {name}:")
        print(f"     Mean:   {np.mean(data):.3f} s")
        print(f"     Std:    {np.std(data, ddof=1):.3f} s")
        print(f"     Median: {np.median(data):.3f} s")
        print(f"     Min:    {np.min(data):.3f} s")
        print(f"     Max:    {np.max(data):.3f} s")
        print(f"     CV:     {np.std(data,ddof=1)/np.mean(data)*100:.1f}%")

    # Test assumptions
    print(f"\n4. Assumption Testing:")
    print("-" * 70)

    suite = StatisticalTestSuite(StatisticalTestConfig(
        significance_level=alpha,
        normality_tests=['shapiro', 'anderson']
    ))

    # Test normality for each controller
    print("\n   Normality Tests (Shapiro-Wilk):")
    normality_ok = {}
    for name, data in controllers.items():
        result = suite.validate(data, test_types=['normality_tests'])
        if result.status.name == 'SUCCESS':
            shapiro = result.data['normality_tests']['shapiro_wilk']
            p_val = shapiro['p_value']
            normal = p_val > alpha
            normality_ok[name] = normal

            status = "✓ Normal" if normal else "✗ Non-normal"
            print(f"     {name:20s}: W={shapiro['statistic']:.4f}, "
                  f"p={p_val:.4f} {status}")

    # Test homogeneity of variances (Levene's test)
    print("\n   Homogeneity of Variance (Levene's test):")
    levene_stat, levene_p = stats.levene(classical_data, supertwisting_data, adaptive_data)
    homoscedastic = levene_p > alpha
    print(f"     F={levene_stat:.4f}, p={levene_p:.4f}")
    if homoscedastic:
        print(f"     ✓ Equal variances assumption satisfied")
    else:
        print(f"     ⚠ Unequal variances - will use Welch's test")

    # Pairwise comparisons
    print(f"\n5. Pairwise Comparisons:")
    print("-" * 70)

    comparisons = [
        ('Classical SMC', 'Super-Twisting SMC', classical_data, supertwisting_data),
        ('Classical SMC', 'Adaptive SMC', classical_data, adaptive_data),
        ('Super-Twisting SMC', 'Adaptive SMC', supertwisting_data, adaptive_data)
    ]

    # Bonferroni correction for multiple comparisons
    alpha_corrected = alpha / len(comparisons)
    print(f"\n   Multiple comparison correction: Bonferroni")
    print(f"   Corrected significance level: α={alpha_corrected:.4f}")

    significant_pairs = []

    for name1, name2, data1, data2 in comparisons:
        print(f"\n   {name1} vs {name2}:")

        # Independent t-test (Welch's if unequal variances)
        equal_var = homoscedastic
        t_stat, t_p = stats.ttest_ind(data1, data2, equal_var=equal_var)

        test_type = "Independent t-test" if equal_var else "Welch's t-test"
        print(f"     {test_type}:")
        print(f"       t={t_stat:.4f}, p={t_p:.4f}")

        significant = t_p < alpha_corrected
        if significant:
            print(f"       ✓ SIGNIFICANT (p < {alpha_corrected:.4f})")
            significant_pairs.append((name1, name2))
        else:
            print(f"       ✗ Not significant")

        # Mann-Whitney U test (non-parametric alternative)
        u_stat, u_p = stats.mannwhitneyu(data1, data2, alternative='two-sided')
        print(f"     Mann-Whitney U test (non-parametric):")
        print(f"       U={u_stat:.1f}, p={u_p:.4f}")

        # Effect size (Cohen's d)
        effect_size = compute_effect_size_cohens_d(data1, data2)
        print(f"     Effect Size (Cohen's d):")
        print(f"       d={effect_size['d']:.3f} ({effect_size['interpretation']})")
        print(f"       Mean difference: {effect_size['mean_diff']:.3f} s")

        # Confidence interval for mean difference
        ci_lower, ci_upper = stats.t.interval(
            0.95,
            len(data1) + len(data2) - 2,
            loc=np.mean(data1) - np.mean(data2),
            scale=effect_size['pooled_std'] * np.sqrt(1/len(data1) + 1/len(data2))
        )
        print(f"       95% CI for difference: [{ci_lower:.3f}, {ci_upper:.3f}] s")

    # One-way ANOVA
    print(f"\n6. Omnibus Test (One-Way ANOVA):")
    print("-" * 70)

    f_stat, anova_p = stats.f_oneway(classical_data, supertwisting_data, adaptive_data)
    print(f"   F={f_stat:.4f}, p={anova_p:.6f}")

    if anova_p < alpha:
        print(f"   ✓ SIGNIFICANT: At least one controller differs")
    else:
        print(f"   ✗ Not significant: No evidence of difference")

    # Kruskal-Wallis (non-parametric alternative)
    h_stat, kw_p = stats.kruskal(classical_data, supertwisting_data, adaptive_data)
    print(f"\n   Kruskal-Wallis test (non-parametric):")
    print(f"   H={h_stat:.4f}, p={kw_p:.6f}")

    # Power analysis
    print(f"\n7. Power Analysis:")
    print("-" * 70)

    for name1, name2, data1, data2 in comparisons:
        effect_size = compute_effect_size_cohens_d(data1, data2)
        d = abs(effect_size['d'])

        # Calculate power (simplified - using normal approximation)
        from scipy.stats import norm
        n = len(data1)  # Assume equal sample sizes
        ncp = d * np.sqrt(n / 2)  # Non-centrality parameter

        # Two-tailed test power
        z_crit = norm.ppf(1 - alpha_corrected/2)
        power = 1 - norm.cdf(z_crit - ncp) + norm.cdf(-z_crit - ncp)

        print(f"\n   {name1} vs {name2}:")
        print(f"     Effect size (d): {d:.3f}")
        print(f"     Sample size (n): {n}")
        print(f"     Power: {power:.3f} ({power*100:.1f}%)")

        if power < 0.8:
            # Calculate required sample size for 80% power
            z_beta = norm.ppf(0.8)
            n_req = 2 * ((z_crit + z_beta) / d)**2
            print(f"     ⚠ Low power - recommend n={int(np.ceil(n_req))} for 80% power")
        else:
            print(f"     ✓ Adequate power (≥80%)")

    # Summary and recommendations
    print(f"\n" + "=" * 70)
    print("CONCLUSIONS:")
    print("=" * 70)

    print(f"\n1. Statistical Significance:")
    if significant_pairs:
        print(f"   Significant differences found (α={alpha_corrected:.4f}):")
        for name1, name2 in significant_pairs:
            print(f"     - {name1} vs {name2}")
    else:
        print(f"   No significant differences detected")

    print(f"\n2. Effect Sizes:")
    for name1, name2, data1, data2 in comparisons:
        effect_size = compute_effect_size_cohens_d(data1, data2)
        print(f"   {name1} vs {name2}:")
        print(f"     Cohen's d = {effect_size['d']:.3f} ({effect_size['interpretation']})")

    print(f"\n3. Practical Recommendations:")

    # Rank controllers
    mean_times = {name: np.mean(data) for name, data in controllers.items()}
    ranked = sorted(mean_times.items(), key=lambda x: x[1])

    print(f"   Performance ranking (by mean settling time):")
    for rank, (name, mean_time) in enumerate(ranked, 1):
        print(f"     {rank}. {name:20s}: {mean_time:.3f} s")

    best_controller = ranked[0][0]
    print(f"\n   ✓ RECOMMENDED: {best_controller}")
    print(f"     - Fastest mean settling time")

    # Check if best is significantly better than others
    best_data = controllers[best_controller]
    significant_improvement = False
    for name, data in controllers.items():
        if name != best_controller:
            t_stat, t_p = stats.ttest_ind(best_data, data, equal_var=False)
            if t_p < alpha_corrected:
                effect_size = compute_effect_size_cohens_d(best_data, data)
                print(f"     - Significantly better than {name} "
                      f"(p={t_p:.4f}, d={abs(effect_size['d']):.3f})")
                significant_improvement = True

    if not significant_improvement:
        print(f"     ⚠ Note: Improvement not statistically significant")
        print(f"       Consider cost-benefit analysis for deployment")

    print("=" * 70)


if __name__ == "__main__":
    main()