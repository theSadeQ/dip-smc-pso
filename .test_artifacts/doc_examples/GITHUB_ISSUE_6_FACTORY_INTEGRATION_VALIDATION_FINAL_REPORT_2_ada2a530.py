# Example from: docs\reports\GITHUB_ISSUE_6_FACTORY_INTEGRATION_VALIDATION_FINAL_REPORT.md
# Index: 2
# Runnable: False
# Hash: ada2a530

# example-metadata:
# runnable: false

# Validated PSO Integration:
- PSOTuner import: ✅ Successful
- create_smc_for_pso(): ✅ Functional
- PSO wrapper creation: ✅ All controller types supported
- Control computation: ✅ Verified outputs

# PSO Test Results:
- Classical SMC PSO wrapper: ✅ Control output: [-49.0]
- Adaptive SMC PSO wrapper: ✅ Control output: [-20.25]
- STA SMC PSO wrapper: ✅ Control output: [-75.83]
- Hybrid SMC PSO wrapper: ⚠️ NoneType issue detected