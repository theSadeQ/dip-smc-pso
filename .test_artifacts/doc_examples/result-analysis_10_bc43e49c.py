# Example from: docs\guides\how-to\result-analysis.md
# Index: 10
# Runnable: True
# Hash: bc43e49c

from scipy.stats import bootstrap

# Bootstrap confidence interval (more robust, no normality assumption)
def compute_mean(data, axis):
    return np.mean(data, axis=axis)

# Classical SMC bootstrap CI
bootstrap_result_classical = bootstrap(
    (ise_classical_trials,),
    compute_mean,
    n_resamples=10000,
    confidence_level=0.95,
    method='percentile'
)

print(f"\nBootstrap 95% CI (Classical): "
      f"[{bootstrap_result_classical.confidence_interval.low:.4f}, "
      f"{bootstrap_result_classical.confidence_interval.high:.4f}]")