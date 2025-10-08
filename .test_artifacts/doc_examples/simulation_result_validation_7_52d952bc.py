# Example from: docs\validation\simulation_result_validation.md
# Index: 7
# Runnable: True
# Hash: 52d952bc

config = MonteCarloConfig(
    bootstrap_samples=1000,
    bootstrap_confidence_level=0.95
)

result = analyzer.validate(data)
bootstrap_ci = result.data['bootstrap_analysis']['mean_confidence_interval']