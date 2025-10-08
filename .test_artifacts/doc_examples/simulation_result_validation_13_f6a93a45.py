# Example from: docs\validation\simulation_result_validation.md
# Index: 13
# Runnable: True
# Hash: f6a93a45

config = CrossValidationConfig(
    cv_method="monte_carlo",
    n_repetitions=100,
    test_ratio=0.2,
    random_state=42
)