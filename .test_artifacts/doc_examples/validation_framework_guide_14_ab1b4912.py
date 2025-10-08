# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 14
# Runnable: True
# Hash: ab1b4912

from tests.test_integration.test_end_to_end_validation import EndToEndWorkflowValidator

validator = EndToEndWorkflowValidator()

# Validate CLI accessibility
cli_result = validator.validate_cli_accessibility()

print(f"CLI Validation: {'✅ PASS' if cli_result.success else '❌ FAIL'}")
print(f"Execution time: {cli_result.execution_time:.2f}s")
print(f"Steps completed:")
for step in cli_result.steps_completed:
    print(f"  ✓ {step}")

if cli_result.error_messages:
    print(f"Errors:")
    for error in cli_result.error_messages:
        print(f"  ✗ {error}")

# Validate configuration system
config_result = validator.validate_configuration_system()

# Validate simulation execution
sim_result = validator.validate_simulation_execution()

# Overall system validation
print("\n=== System Validation Summary ===")
print(f"CLI Accessibility: {cli_result.success}")
print(f"Configuration: {config_result.success}")
print(f"Simulation: {sim_result.success}")

success_rate = sum([cli_result.success, config_result.success, sim_result.success]) / 3
production_ready = success_rate >= 0.95

print(f"\nSuccess Rate: {success_rate*100:.1f}%")
print(f"Production Ready: {'✅ YES' if production_ready else '❌ NO'}")