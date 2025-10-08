# Example from: docs\validation\simulation_result_validation.md
# Index: 16
# Runnable: True
# Hash: 4a6c870b

result = validator.validate(data, models=[model])
lc = result.data['learning_curve_analysis'][model_name]

train_sizes = lc['train_sizes']
train_scores = lc['train_scores']
test_scores = lc['test_scores']