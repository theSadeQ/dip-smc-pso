# plant.models.base.dynamics_interface

**Source:** `src\plant\models\base\dynamics_interface.py`

## Module Overview

Common interface for plant dynamics models.

Defines abstract base classes and protocols that ensure consistency
across different dynamics implementations (simplified, full, low-rank).

## Complete Source Code

```{literalinclude} ../../../src/plant/models/base/dynamics_interface.py
:language: python
:linenos:
```

---

## Classes

### `IntegrationMethod`

**Inherits from:** `Enum`

Available integration methods for dynamics.

#### Source Code

```{literalinclude} ../../../src/plant/models/base/dynamics_interface.py
:language: python
:pyobject: IntegrationMethod
:linenos:
```

---

### `DynamicsResult`

**Inherits from:** `NamedTuple`

Result of dynamics computation.

Contains state derivatives and optional diagnostic information
for debugging and analysis.

#### Source Code

```{literalinclude} ../../../src/plant/models/base/dynamics_interface.py
:language: python
:pyobject: DynamicsResult
:linenos:
```

#### Methods (2)

##### `success_result(cls, state_derivative)`

Create successful dynamics result.

[View full source →](#method-dynamicsresult-success_result)

##### `failure_result(cls, reason)`

Create failed dynamics result.

[View full source →](#method-dynamicsresult-failure_result)

---

### `DynamicsModel`

**Inherits from:** `Protocol`

Protocol for plant dynamics models.

Defines the interface that all dynamics models must implement
for consistent integration with controllers and simulators.

#### Source Code

```{literalinclude} ../../../src/plant/models/base/dynamics_interface.py
:language: python
:pyobject: DynamicsModel
:linenos:
```

#### Methods (5)

##### `compute_dynamics(self, state, control_input, time)`

Compute system dynamics at given state and input.

[View full source →](#method-dynamicsmodel-compute_dynamics)

##### `get_physics_matrices(self, state)`

Get physics matrices M, C, G at current state.

[View full source →](#method-dynamicsmodel-get_physics_matrices)

##### `validate_state(self, state)`

Validate state vector format and bounds.

[View full source →](#method-dynamicsmodel-validate_state)

##### `get_state_dimension(self)`

Get the dimension of the state vector.

[View full source →](#method-dynamicsmodel-get_state_dimension)

##### `get_control_dimension(self)`

Get the dimension of the control input vector.

[View full source →](#method-dynamicsmodel-get_control_dimension)

---

### `BaseDynamicsModel`

**Inherits from:** `ABC`

Abstract base class for dynamics models.

Provides common functionality and enforces interface compliance
for concrete dynamics implementations.

#### Source Code

```{literalinclude} ../../../src/plant/models/base/dynamics_interface.py
:language: python
:pyobject: BaseDynamicsModel
:linenos:
```

#### Methods (14)

##### `__init__(self, parameters)`

Initialize dynamics model.

[View full source →](#method-basedynamicsmodel-__init__)

##### `compute_dynamics(self, state, control_input, time)`

Compute system dynamics (must be implemented by subclasses).

[View full source →](#method-basedynamicsmodel-compute_dynamics)

##### `get_physics_matrices(self, state)`

Get physics matrices (must be implemented by subclasses).

[View full source →](#method-basedynamicsmodel-get_physics_matrices)

##### `_setup_validation(self)`

Setup state validation (must be implemented by subclasses).

[View full source →](#method-basedynamicsmodel-_setup_validation)

##### `validate_state(self, state)`

Validate state vector using configured validator.

[View full source →](#method-basedynamicsmodel-validate_state)

##### `sanitize_state(self, state)`

Sanitize state vector if validator supports it.

[View full source →](#method-basedynamicsmodel-sanitize_state)

##### `get_state_dimension(self)`

Get state vector dimension (default: 6 for DIP).

[View full source →](#method-basedynamicsmodel-get_state_dimension)

##### `get_control_dimension(self)`

Get control input dimension (default: 1 for DIP).

[View full source →](#method-basedynamicsmodel-get_control_dimension)

##### `reset_monitoring(self)`

Reset monitoring statistics.

[View full source →](#method-basedynamicsmodel-reset_monitoring)

##### `get_monitoring_stats(self)`

Get monitoring statistics.

[View full source →](#method-basedynamicsmodel-get_monitoring_stats)

##### `_setup_monitoring(self)`

Setup default monitoring (can be overridden).

[View full source →](#method-basedynamicsmodel-_setup_monitoring)

##### `_basic_state_validation(self, state)`

Basic state validation fallback.

[View full source →](#method-basedynamicsmodel-_basic_state_validation)

##### `_create_success_result(self, state_derivative)`

Helper to create successful dynamics result.

[View full source →](#method-basedynamicsmodel-_create_success_result)

##### `_create_failure_result(self, reason)`

Helper to create failed dynamics result.

[View full source →](#method-basedynamicsmodel-_create_failure_result)

---

### `LinearDynamicsModel`

**Inherits from:** `BaseDynamicsModel`

Base class for linear dynamics models.

Provides structure for linear systems of the form:
ẋ = Ax + Bu + f(t)

Where A is the system matrix, B is the input matrix,
and f(t) is an optional time-varying disturbance.

#### Source Code

```{literalinclude} ../../../src/plant/models/base/dynamics_interface.py
:language: python
:pyobject: LinearDynamicsModel
:linenos:
```

#### Methods (6)

##### `__init__(self, A, B, parameters)`

Initialize linear dynamics model.

[View full source →](#method-lineardynamicsmodel-__init__)

##### `compute_dynamics(self, state, control_input, time)`

Compute linear dynamics.

[View full source →](#method-lineardynamicsmodel-compute_dynamics)

##### `get_physics_matrices(self, state)`

Get linear system matrices as M, C, G equivalent.

[View full source →](#method-lineardynamicsmodel-get_physics_matrices)

##### `_setup_validation(self)`

Setup validation for linear systems.

[View full source →](#method-lineardynamicsmodel-_setup_validation)

##### `_validate_matrices(self)`

Validate system matrices.

[View full source →](#method-lineardynamicsmodel-_validate_matrices)

##### `_validate_control_input(self, control_input)`

Validate control input vector.

[View full source →](#method-lineardynamicsmodel-_validate_control_input)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Protocol, Tuple, Optional, Dict, Any, NamedTuple`
- `from abc import ABC, abstractmethod`
- `from enum import Enum`
- `import numpy as np`
