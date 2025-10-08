# Example from: docs\validation\simulation_result_validation.md
# Index: 11
# Runnable: True
# Hash: e3845e7f

config = CrossValidationConfig(
    cv_method="time_series",
    n_splits=5,
    max_train_size=None,  # Use all past data
    test_size=None,       # Auto-determined
    gap=0                 # No gap between train/test
)
validator = CrossValidator(config)