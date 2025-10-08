# Example from: docs\factory\configuration_reference.md
# Index: 19
# Runnable: True
# Hash: b759a6f5

# Quality gates enforced by factory
assert coverage >= 0.95  # 95% test coverage for critical components
assert thread_safety_tests_pass == True
assert memory_leak_tests_pass == True
assert performance_constraints_met == True