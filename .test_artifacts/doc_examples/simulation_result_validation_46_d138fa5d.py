# Example from: docs\validation\simulation_result_validation.md
# Index: 46
# Runnable: False
# Hash: d138fa5d

# Monte Carlo + Cross-Validation + Statistical Tests
mc_result = mc_analyzer.validate(...)
cv_result = cv_validator.validate(...)
stat_result = stat_suite.validate(...)

# If all agree → high confidence
# If diverge → investigate why