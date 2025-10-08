# Example from: docs\validation\simulation_result_validation.md
# Index: 36
# Runnable: True
# Hash: ba80b18e

from src.analysis.validation.cross_validation import CrossValidator

validator = CrossValidator(CrossValidationConfig(
    cv_method="monte_carlo",
    n_repetitions=50,
    test_ratio=0.2
))

# For each CV split:
#   - Optimize on training scenarios
#   - Evaluate on test scenarios
#   - Record generalization gap

cv_result = validator.validate(
    scenarios,
    models=[pso_optimized_controller],
    prediction_function=simulate_controller
)

generalization_gap = (
    cv_result.data['monte_carlo_validation']['training_score'] -
    cv_result.data['monte_carlo_validation']['test_score']
)

if generalization_gap > threshold:
    print("⚠ Overfitting detected - need more diverse training scenarios")