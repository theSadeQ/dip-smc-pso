# Example from: docs\validation\simulation_result_validation.md
# Index: 37
# Runnable: True
# Hash: b637ee21

config = CrossValidationConfig(
    cv_method="time_series",
    n_splits=5,
    max_train_size=100,  # Limit adaptation window
    gap=10               # Predict 10 steps ahead
)

# Each fold:
#   - Controller adapts on [t₀, t₁]
#   - Performance evaluated on [t₁+gap, t₂]