# Example from: docs\guides\api\utilities.md
# Index: 17
# Runnable: True
# Hash: 1aea0d62

from src.utils.analysis import compute_confidence_interval

# Monte Carlo results
ise_values = [result['metrics']['ise'] for result in monte_carlo_results]

mean, ci_lower, ci_upper = compute_confidence_interval(
    ise_values,
    confidence=0.95
)

print(f"ISE: {mean:.4f} [{ci_lower:.4f}, {ci_upper:.4f}] (95% CI)")