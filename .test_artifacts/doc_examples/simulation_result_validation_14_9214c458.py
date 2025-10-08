# Example from: docs\validation\simulation_result_validation.md
# Index: 14
# Runnable: True
# Hash: 9214c458

config = CrossValidationConfig(
    cv_method="k_fold",
    n_splits=5,              # Outer CV
    enable_nested_cv=True,
    inner_cv_splits=3        # Inner CV
)