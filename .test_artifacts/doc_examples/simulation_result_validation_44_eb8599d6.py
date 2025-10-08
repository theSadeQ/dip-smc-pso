# Example from: docs\validation\simulation_result_validation.md
# Index: 44
# Runnable: True
# Hash: eb8599d6

# Use nested CV for unbiased evaluation
config = CrossValidationConfig(
    enable_nested_cv=True,
    n_splits=5,
    inner_cv_splits=3
)