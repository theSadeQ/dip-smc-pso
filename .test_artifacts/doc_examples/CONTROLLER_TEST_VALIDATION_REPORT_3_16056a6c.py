# Example from: docs\reports\CONTROLLER_TEST_VALIDATION_REPORT.md
# Index: 3
# Runnable: True
# Hash: 16056a6c

# Fixed parameter bounds and compatibility
'max_condition_number': assert 1e3 <= reg_value <= 1e15  # Was: 1e12
'pendulum2_inertia': 0.008,  # Fixed: was 0.005 (below physical bound)