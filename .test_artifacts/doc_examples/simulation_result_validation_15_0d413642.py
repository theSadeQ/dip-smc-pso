# Example from: docs\validation\simulation_result_validation.md
# Index: 15
# Runnable: True
# Hash: 0d413642

result = validator.validate(
    data,
    models=[model],
    prediction_function=predict_fn
)
bv_analysis = result.data['bias_variance_analysis']

bias_squared = bv_analysis[model_name]['bias_squared']
variance = bv_analysis[model_name]['variance']