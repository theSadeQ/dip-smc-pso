# Example from: docs\validation\simulation_result_validation.md
# Index: 10
# Runnable: True
# Hash: 0a6aded0

from src.analysis.validation.cross_validation import CrossValidationConfig, CrossValidator

config = CrossValidationConfig(
    cv_method="k_fold",
    n_splits=5,
    shuffle=True,
    random_state=42
)
validator = CrossValidator(config)