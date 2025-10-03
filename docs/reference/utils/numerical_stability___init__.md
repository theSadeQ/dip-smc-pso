# utils.numerical_stability.__init__

**Source:** `src\utils\numerical_stability\__init__.py`

## Module Overview

Numerical stability utilities for robust mathematical operations.

This module provides safe mathematical operations that protect against:
- Division by zero and near-zero denominators
- Negative arguments to sqrt and log
- Numerical overflow/underflow
- Catastrophic cancellation

All operations use configurable epsilon thresholds tuned for control system
stability and optimization algorithm convergence.

Example:
    >>> from src.utils.numerical_stability import safe_divide, safe_sqrt
    >>> result = safe_divide(1.0, 1e-15)  # Protected division
    >>> root = safe_sqrt(-0.001)  # Safe sqrt with negative protection

## Complete Source Code

```{literalinclude} ../../../src/utils/numerical_stability/__init__.py
:language: python
:linenos:
```

---

## Dependencies

This module imports:

- `from src.utils.numerical_stability.safe_operations import safe_divide, safe_reciprocal, safe_sqrt, safe_log, safe_exp, safe_power, safe_norm, safe_normalize, EPSILON_DIV, EPSILON_SQRT, EPSILON_LOG, EPSILON_EXP, is_safe_denominator, clip_to_safe_range`
