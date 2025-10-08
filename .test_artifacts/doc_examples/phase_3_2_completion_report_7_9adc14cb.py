# Example from: docs\benchmarks\phase_3_2_completion_report.md
# Index: 7
# Runnable: False
# Hash: 9adc14cb

# example-metadata:
# runnable: false

# PSO optimizer expects:
fitness = evaluate_controller_gains(gains_array)

# Hybrid controller provides:
config = HybridSMCConfig(classical_gains=[...], sta_gains=[...], ...)
# But config.gains doesn't exist → PSO can't access/optimize