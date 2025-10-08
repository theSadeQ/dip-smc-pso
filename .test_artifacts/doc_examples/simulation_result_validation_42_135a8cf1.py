# Example from: docs\validation\simulation_result_validation.md
# Index: 42
# Runnable: True
# Hash: 135a8cf1

# For time series, ALWAYS use time series CV
config = CrossValidationConfig(
    cv_method="time_series"  # Not "k_fold"!
)