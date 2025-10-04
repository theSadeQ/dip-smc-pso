# plant.models.simplified.dynamics

**Source:** `src\plant\models\simplified\dynamics.py`

## Module Overview

Simplified DIP Dynamics Model.

Main dynamics model implementation combining all simplified DIP components.
Provides a clean, modular interface for the simplified double inverted
pendulum dynamics with numerical stability and performance optimizations.

## Complete Source Code

```{literalinclude} ../../../src/plant/models/simplified/dynamics.py
:language: python
:linenos:
```

---

## Classes

### `SimplifiedDIPDynamics`

**Inherits from:** `BaseDynamicsModel`

Simplified Double Inverted Pendulum Dynamics Model.

Modular implementation of simplified DIP dynamics featuring:
- Type-safe configuration with validation
- Numerical stability monitoring and recovery
- Performance optimizations with JIT compilation
- Clean separation of physics computation
- Comprehensive state validation

#### Source Code

```{literalinclude} ../../../src/plant/models/simplified/dynamics.py
:language: python
:pyobject: SimplifiedDIPDynamics
:linenos:
```

#### Methods (17)

##### `__init__(self, config, enable_fast_mode, enable_monitoring)`

Initialize simplified DIP dynamics.

[View full source →](#method-simplifieddipdynamics-__init__)

##### `_filter_config_for_simplified(self, config_dict)`

Filter configuration dictionary to only include fields accepted by SimplifiedDIPConfig.

[View full source →](#method-simplifieddipdynamics-_filter_config_for_simplified)

##### `compute_dynamics(self, state, control_input, time)`

Compute simplified DIP dynamics.

[View full source →](#method-simplifieddipdynamics-compute_dynamics)

##### `get_physics_matrices(self, state)`

Get physics matrices M, C, G at current state.

[View full source →](#method-simplifieddipdynamics-get_physics_matrices)

##### `compute_total_energy(self, state)`

Compute total system energy.

[View full source →](#method-simplifieddipdynamics-compute_total_energy)

##### `compute_linearization(self, equilibrium_state, equilibrium_input)`

Compute linearization around equilibrium point.

[View full source →](#method-simplifieddipdynamics-compute_linearization)

##### `get_equilibrium_states(self)`

Get standard equilibrium states for the DIP system.

[View full source →](#method-simplifieddipdynamics-get_equilibrium_states)

##### `_setup_validation(self)`

Setup state validation for simplified DIP.

[View full source →](#method-simplifieddipdynamics-_setup_validation)

##### `_compute_standard_dynamics(self, state, control_input)`

Compute dynamics using standard (modular) approach.

[View full source →](#method-simplifieddipdynamics-_compute_standard_dynamics)

##### `_compute_fast_dynamics(self, state, control_input)`

Compute dynamics using fast JIT-compiled approach.

[View full source →](#method-simplifieddipdynamics-_compute_fast_dynamics)

##### `_validate_control_input(self, control_input)`

Validate control input vector.

[View full source →](#method-simplifieddipdynamics-_validate_control_input)

##### `_validate_state_derivative(self, state_derivative)`

Validate computed state derivative.

[View full source →](#method-simplifieddipdynamics-_validate_state_derivative)

##### `_compute_linearization_matrices(self, eq_state, eq_input)`

Compute linearization matrices A, B.

[View full source →](#method-simplifieddipdynamics-_compute_linearization_matrices)

##### `_record_successful_computation(self, state)`

Record successful computation for monitoring.

[View full source →](#method-simplifieddipdynamics-_record_successful_computation)

##### `_record_numerical_instability(self, state)`

Record numerical instability for monitoring.

[View full source →](#method-simplifieddipdynamics-_record_numerical_instability)

##### `_record_computation_failure(self, state)`

Record general computation failure for monitoring.

[View full source →](#method-simplifieddipdynamics-_record_computation_failure)

##### `_rhs_core(self, state, u)`

Compatibility method for legacy code expecting _rhs_core.

[View full source →](#method-simplifieddipdynamics-_rhs_core)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Tuple, Optional, Dict, Any, Union`
- `import numpy as np`
- `import warnings`
- `from ..base import BaseDynamicsModel, DynamicsResult`
- `from ...core import DIPStateValidator, NumericalInstabilityError, NumericalStabilityMonitor`
- `from .config import SimplifiedDIPConfig`
- `from .physics import SimplifiedPhysicsComputer, compute_simplified_dynamics_numba`
