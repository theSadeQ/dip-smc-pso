# Example from: docs\validation\validation_examples.md
# Index: 8
# Runnable: False
# Hash: 35c6a23b

# example-metadata:
# runnable: false

"""
Uncertainty Quantification for Settling Time Predictions
=========================================================

This script demonstrates comprehensive uncertainty quantification including:
- Bootstrap confidence intervals
- Distribution fitting
- Risk analysis (VaR, CVaR)
- Probabilistic guarantees
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from src.analysis.validation.monte_carlo import MonteCarloConfig, MonteCarloAnalyzer

# Random seed
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)


def generate_settling_time_data(n_samples: int = 200) -> np.ndarray:
    """
    Generate realistic settling time data (log-normal distribution).

    Parameters
    ----------
    n_samples : int
        Number of samples

    Returns
    -------
    np.ndarray
        Settling times in seconds
    """
    # Log-normal distribution (realistic for settling times - positive skew)
    # ln(T) ~ N(μ, σ²)
    mu = 0.7  # log-scale mean
    sigma = 0.3  # log-scale std

    settling_times = np.random.lognormal(mu, sigma, n_samples)

    return settling_times


def main():
    """Main uncertainty quantification script."""

    print("=" * 70)
    print("Uncertainty Quantification for Settling Time")
    print("=" * 70)

    # Safety requirement
    SAFETY_THRESHOLD = 3.0  # seconds
    REQUIRED_CONFIDENCE = 0.99  # 99% confidence

    print(f"\n1. Safety Requirement:")
    print(f"   Settling time must be < {SAFETY_THRESHOLD}s with {REQUIRED_CONFIDENCE*100}% confidence")

    # Generate data
    n_samples = 200
    print(f"\n2. Collecting experimental data...")
    print(f"   Number of test runs: {n_samples}")

    settling_times = generate_settling_time_data(n_samples)

    # Basic statistics
    print(f"\n3. Descriptive Statistics:")
    print("-" * 70)
    print(f"   Mean:     {np.mean(settling_times):.3f} s")
    print(f"   Std:      {np.std(settling_times, ddof=1):.3f} s")
    print(f"   Median:   {np.median(settling_times):.3f} s")
    print(f"   Min:      {np.min(settling_times):.3f} s")
    print(f"   Max:      {np.max(settling_times):.3f} s")
    print(f"   Range:    {np.max(settling_times) - np.min(settling_times):.3f} s")

    # Percentiles
    print(f"\n   Percentiles:")
    percentiles = [5, 25, 50, 75, 95, 99]
    for p in percentiles:
        value = np.percentile(settling_times, p)
        print(f"     {p:2d}%: {value:.3f} s")

    # Bootstrap confidence intervals
    print(f"\n4. Bootstrap Confidence Intervals:")
    print("-" * 70)

    n_bootstrap = 10000
    bootstrap_means = []
    bootstrap_medians = []
    bootstrap_stds = []
    bootstrap_95th = []

    for _ in range(n_bootstrap):
        bootstrap_sample = np.random.choice(settling_times, size=len(settling_times), replace=True)
        bootstrap_means.append(np.mean(bootstrap_sample))
        bootstrap_medians.append(np.median(bootstrap_sample))
        bootstrap_stds.append(np.std(bootstrap_sample, ddof=1))
        bootstrap_95th.append(np.percentile(bootstrap_sample, 95))

    # Compute bootstrap CIs
    ci_level = 0.95
    alpha = 1 - ci_level

    mean_ci = [
        np.percentile(bootstrap_means, 100 * alpha/2),
        np.percentile(bootstrap_means, 100 * (1 - alpha/2))
    ]

    median_ci = [
        np.percentile(bootstrap_medians, 100 * alpha/2),
        np.percentile(bootstrap_medians, 100 * (1 - alpha/2))
    ]

    percentile_95_ci = [
        np.percentile(bootstrap_95th, 100 * alpha/2),
        np.percentile(bootstrap_95th, 100 * (1 - alpha/2))
    ]

    print(f"   Bootstrap iterations: {n_bootstrap}")
    print(f"   Confidence level: {ci_level*100}%")
    print(f"\n   Mean settling time:")
    print(f"     Point estimate: {np.mean(settling_times):.3f} s")
    print(f"     95% CI: [{mean_ci[0]:.3f}, {mean_ci[1]:.3f}] s")
    print(f"     CI width: {mean_ci[1] - mean_ci[0]:.3f} s")

    print(f"\n   Median settling time:")
    print(f"     Point estimate: {np.median(settling_times):.3f} s")
    print(f"     95% CI: [{median_ci[0]:.3f}, {median_ci[1]:.3f}] s")

    print(f"\n   95th percentile:")
    print(f"     Point estimate: {np.percentile(settling_times, 95):.3f} s")
    print(f"     95% CI: [{percentile_95_ci[0]:.3f}, {percentile_95_ci[1]:.3f}] s")

    # Distribution fitting
    print(f"\n5. Distribution Fitting:")
    print("-" * 70)

    distributions = {
        'Normal': stats.norm,
        'Lognormal': stats.lognorm,
        'Gamma': stats.gamma,
        'Exponential': stats.expon
    }

    fit_results = {}

    for dist_name, dist in distributions.items():
        try:
            # Fit distribution
            if dist_name == 'Exponential':
                params = dist.fit(settling_times, floc=0)
            else:
                params = dist.fit(settling_times)

            # Kolmogorov-Smirnov test
            ks_stat, ks_p = stats.kstest(settling_times, lambda x: dist.cdf(x, *params))

            # AIC (Akaike Information Criterion)
            log_likelihood = np.sum(dist.logpdf(settling_times, *params))
            aic = 2 * len(params) - 2 * log_likelihood

            fit_results[dist_name] = {
                'params': params,
                'ks_stat': ks_stat,
                'ks_p': ks_p,
                'aic': aic
            }

            print(f"\n   {dist_name}:")
            print(f"     K-S statistic: {ks_stat:.4f}")
            print(f"     p-value: {ks_p:.4f}")
            print(f"     AIC: {aic:.2f}")

            if ks_p > 0.05:
                print(f"     ✓ Cannot reject (good fit)")
            else:
                print(f"     ✗ Reject (poor fit)")

        except Exception as e:
            print(f"\n   {dist_name}: Fitting failed ({str(e)})")

    # Best fit (lowest AIC)
    valid_fits = {k: v for k, v in fit_results.items() if 'aic' in v}
    if valid_fits:
        best_fit_name = min(valid_fits.keys(), key=lambda k: valid_fits[k]['aic'])
        best_fit = valid_fits[best_fit_name]

        print(f"\n   Best fit (lowest AIC): {best_fit_name}")
        print(f"     AIC = {best_fit['aic']:.2f}")

    # Risk analysis
    print(f"\n6. Risk Analysis:")
    print("-" * 70)

    # Value at Risk (VaR)
    risk_levels = [0.01, 0.05, 0.10]

    print(f"\n   Value at Risk (VaR):")
    for alpha_risk in risk_levels:
        var = np.percentile(settling_times, (1-alpha_risk)*100)
        print(f"     VaR({alpha_risk*100:.0f}%): {var:.3f} s  (top {alpha_risk*100}% worst cases)")

    # Conditional Value at Risk (CVaR / Expected Shortfall)
    print(f"\n   Conditional Value at Risk (CVaR / Expected Shortfall):")
    for alpha_risk in risk_levels:
        var = np.percentile(settling_times, (1-alpha_risk)*100)
        tail_values = settling_times[settling_times >= var]
        cvar = np.mean(tail_values) if len(tail_values) > 0 else var
        print(f"     CVaR({alpha_risk*100:.0f}%): {cvar:.3f} s  (avg of worst {alpha_risk*100}%)")

    # Safety validation
    print(f"\n7. Safety Validation:")
    print("-" * 70)

    # Empirical probability
    n_exceeds = np.sum(settling_times > SAFETY_THRESHOLD)
    prob_exceed_empirical = n_exceeds / len(settling_times)

    print(f"\n   Empirical Analysis:")
    print(f"     Samples exceeding {SAFETY_THRESHOLD}s: {n_exceeds}/{len(settling_times)}")
    print(f"     Empirical P(T > {SAFETY_THRESHOLD}s) = {prob_exceed_empirical:.4f} ({prob_exceed_empirical*100:.2f}%)")

    # Bootstrap confidence interval for exceedance probability
    bootstrap_probs = []
    for _ in range(n_bootstrap):
        bootstrap_sample = np.random.choice(settling_times, size=len(settling_times), replace=True)
        prob = np.sum(bootstrap_sample > SAFETY_THRESHOLD) / len(bootstrap_sample)
        bootstrap_probs.append(prob)

    prob_ci = [
        np.percentile(bootstrap_probs, 2.5),
        np.percentile(bootstrap_probs, 97.5)
    ]

    print(f"     95% CI for P(T > {SAFETY_THRESHOLD}s): [{prob_ci[0]:.4f}, {prob_ci[1]:.4f}]")

    # Fitted distribution probability
    if valid_fits:
        best_dist = distributions[best_fit_name]
        prob_exceed_fitted = 1 - best_dist.cdf(SAFETY_THRESHOLD, *best_fit['params'])

        print(f"\n   Fitted {best_fit_name} Distribution:")
        print(f"     P(T > {SAFETY_THRESHOLD}s) = {prob_exceed_fitted:.4f} ({prob_exceed_fitted*100:.2f}%)")

        # Required confidence
        prob_within = 1 - prob_exceed_fitted
        print(f"     P(T ≤ {SAFETY_THRESHOLD}s) = {prob_within:.4f} ({prob_within*100:.2f}%)")

        if prob_within >= REQUIRED_CONFIDENCE:
            print(f"     ✓ PASSES safety requirement ({prob_within*100:.1f}% ≥ {REQUIRED_CONFIDENCE*100}%)")
        else:
            print(f"     ✗ FAILS safety requirement ({prob_within*100:.1f}% < {REQUIRED_CONFIDENCE*100}%)")

            # Calculate required improvement
            target_percentile = best_dist.ppf(REQUIRED_CONFIDENCE, *best_fit['params'])
            print(f"\n     To meet {REQUIRED_CONFIDENCE*100}% confidence:")
            print(f"       Target: {REQUIRED_CONFIDENCE*100}% percentile = {target_percentile:.3f} s")
            print(f"       Required: {target_percentile:.3f}s < {SAFETY_THRESHOLD}s")

            if target_percentile >= SAFETY_THRESHOLD:
                improvement_needed = target_percentile - SAFETY_THRESHOLD
                print(f"       ⚠ Need to improve {REQUIRED_CONFIDENCE*100}% percentile by {improvement_needed:.3f}s")

    # Extreme value analysis
    print(f"\n8. Extreme Value Analysis:")
    print("-" * 70)

    # Block maxima method
    block_size = 20
    n_blocks = len(settling_times) // block_size
    block_maxima = [np.max(settling_times[i*block_size:(i+1)*block_size]) for i in range(n_blocks)]

    # Fit GEV distribution to block maxima
    try:
        gev_params = stats.genextreme.fit(block_maxima)

        print(f"   Block Maxima Method:")
        print(f"     Block size: {block_size}")
        print(f"     Number of blocks: {n_blocks}")
        print(f"     GEV parameters: ξ={gev_params[0]:.3f}, μ={gev_params[1]:.3f}, σ={gev_params[2]:.3f}")

        # Return levels
        return_periods = [10, 50, 100]
        print(f"\n     Return Levels:")
        for period in return_periods:
            return_level = stats.genextreme.ppf(1 - 1/period, *gev_params)
            print(f"       {period}-run worst-case: {return_level:.3f} s")

    except Exception as e:
        print(f"   Extreme value analysis failed: {str(e)}")

    # Summary
    print(f"\n" + "=" * 70)
    print("UNCERTAINTY QUANTIFICATION SUMMARY:")
    print("=" * 70)

    print(f"\n1. Point Estimates:")
    print(f"   Mean: {np.mean(settling_times):.3f} s")
    print(f"   95th percentile: {np.percentile(settling_times, 95):.3f} s")
    print(f"   99th percentile: {np.percentile(settling_times, 99):.3f} s")

    print(f"\n2. Uncertainty (95% CI):")
    print(f"   Mean: [{mean_ci[0]:.3f}, {mean_ci[1]:.3f}] s")
    print(f"   95th percentile: [{percentile_95_ci[0]:.3f}, {percentile_95_ci[1]:.3f}] s")

    print(f"\n3. Distributional Model:")
    if valid_fits:
        print(f"   Best fit: {best_fit_name}")
        print(f"   Goodness-of-fit p-value: {best_fit['ks_p']:.4f}")

    print(f"\n4. Safety Assessment:")
    print(f"   Threshold: {SAFETY_THRESHOLD}s")
    print(f"   Required confidence: {REQUIRED_CONFIDENCE*100}%")
    if valid_fits:
        if prob_within >= REQUIRED_CONFIDENCE:
            print(f"   ✓ PASSES: {prob_within*100:.1f}% of scenarios meet requirement")
        else:
            print(f"   ✗ FAILS: Only {prob_within*100:.1f}% meet requirement")

    print(f"\n5. Recommendations:")
    if prob_within >= REQUIRED_CONFIDENCE:
        print(f"   ✓ Controller ready for safety-critical deployment")
        print(f"   ✓ Uncertainty adequately quantified")
    else:
        print(f"   ✗ Further controller improvement needed")
        print(f"   □ Option 1: Tune controller for better worst-case performance")
        print(f"   □ Option 2: Increase safety threshold")
        print(f"   □ Option 3: Accept lower confidence level (if acceptable)")

    print("=" * 70)


if __name__ == "__main__":
    main()