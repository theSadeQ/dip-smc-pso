# Example from: docs\reference\analysis\validation_statistical_tests.md
# Index: 2
# Runnable: True
# Hash: 2923c213

# Compute confidence intervals
from src.analysis.validation import compute_confidence_interval

ci = compute_confidence_interval(samples, confidence=0.95)
print(f"95% CI: [{ci.lower:.3f}, {ci.upper:.3f}]")