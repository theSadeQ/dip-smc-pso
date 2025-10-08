# Example from: docs\validation\simulation_result_validation.md
# Index: 9
# Runnable: True
# Hash: e8668bac

result = analyzer.validate(data)
dist_analysis = result.data['distribution_analysis']

best_fit = dist_analysis['best_fit']  # e.g., "lognormal"
ks_stat = dist_analysis['distribution_fits'][best_fit]['ks_statistic']
p_value = dist_analysis['distribution_fits'][best_fit]['p_value']