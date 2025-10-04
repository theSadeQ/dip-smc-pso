# plant.core.__init__

**Source:** `src\plant\core\__init__.py`

## Module Overview

Core Plant Components - Shared utilities for plant dynamics.

Provides fundamental building blocks for plant dynamics computation:
- Physics matrix computation (M, C, G matrices)
- Numerical stability and regularization
- State validation and sanitization
- Integration utilities

These components are designed for reuse across different plant models
while maintaining mathematical correctness and numerical robustness.

## Complete Source Code

```{literalinclude} ../../../src/plant/core/__init__.py
:language: python
:linenos:
```

---

## Dependencies

This module imports:

- `from .physics_matrices import PhysicsMatrixComputer, DIPPhysicsMatrices, SimplifiedDIPPhysicsMatrices`
- `from .numerical_stability import NumericalInstabilityError, MatrixRegularizer, AdaptiveRegularizer, MatrixInverter, fast_condition_estimate, NumericalStabilityMonitor`
- `from .state_validation import StateValidationError, StateValidator, DIPStateValidator, MinimalStateValidator`
