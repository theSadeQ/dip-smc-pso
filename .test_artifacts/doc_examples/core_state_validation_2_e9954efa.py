# Example from: docs\reference\plant\core_state_validation.md
# Index: 2
# Runnable: True
# Hash: e9954efa

from src.plant.core.state_validation import *
import numpy as np

# Basic initialization
# Validate state and detect violations
from src.plant.core.state_validation import StateValidator, ValidationResult

validator = StateValidator()
state = np.array([0.0, 0.1, 0.05, 0.0, 0.5, 0.3])

result: ValidationResult = validator.validate(state)
if result.is_valid:
    print("State is physically valid")
else:
    print(f"Violations: {result.violations}")