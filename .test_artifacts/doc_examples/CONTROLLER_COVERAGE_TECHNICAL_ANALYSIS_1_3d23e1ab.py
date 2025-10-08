# Example from: docs\analysis\CONTROLLER_COVERAGE_TECHNICAL_ANALYSIS.md
# Index: 1
# Runnable: False
# Hash: 3d23e1ab

# File: src/controllers/base/control_primitives.py
# Lines: ALL COVERED - safety-critical saturation functions validated
def saturate(sigma, epsilon, method="tanh"):
    # FULL COVERAGE: boundary validation, method selection, error handling

def require_positive(value, name, allow_zero=False):
    # FULL COVERAGE: input validation, error conditions, boundary cases

def require_in_range(value, name, minimum, maximum, allow_equal=True):
    # FULL COVERAGE: range validation, boundary conditions, error handling