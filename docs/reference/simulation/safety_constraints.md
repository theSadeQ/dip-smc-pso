# simulation.safety.constraints

**Source:** `src\simulation\safety\constraints.py`

## Module Overview

Constraint definitions and checking for simulation safety.

## Complete Source Code

```{literalinclude} ../../../src/simulation/safety/constraints.py
:language: python
:linenos:
```

---

## Classes

### `Constraint`

**Inherits from:** `ABC`

Base class for simulation constraints.

#### Source Code

```{literalinclude} ../../../src/simulation/safety/constraints.py
:language: python
:pyobject: Constraint
:linenos:
```

#### Methods (2)

##### `check(self, value)`

Check if constraint is satisfied.

[View full source →](#method-constraint-check)

##### `get_violation_message(self)`

Get constraint violation message.

[View full source →](#method-constraint-get_violation_message)

---

### `StateConstraints`

State variable constraints.

#### Source Code

```{literalinclude} ../../../src/simulation/safety/constraints.py
:language: python
:pyobject: StateConstraints
:linenos:
```

#### Methods (2)

##### `__init__(self, lower_bounds, upper_bounds, custom_constraints)`

Initialize state constraints.

[View full source →](#method-stateconstraints-__init__)

##### `check_all(self, state)`

Check all state constraints.

[View full source →](#method-stateconstraints-check_all)

---

### `ControlConstraints`

Control input constraints.

#### Source Code

```{literalinclude} ../../../src/simulation/safety/constraints.py
:language: python
:pyobject: ControlConstraints
:linenos:
```

#### Methods (2)

##### `__init__(self, min_control, max_control, rate_limit)`

Initialize control constraints.

[View full source →](#method-controlconstraints-__init__)

##### `check_all(self, control, dt)`

Check all control constraints.

[View full source →](#method-controlconstraints-check_all)

---

### `EnergyConstraints`

System energy constraints.

#### Source Code

```{literalinclude} ../../../src/simulation/safety/constraints.py
:language: python
:pyobject: EnergyConstraints
:linenos:
```

#### Methods (2)

##### `__init__(self, max_kinetic, max_potential, max_total)`

Initialize energy constraints.

[View full source →](#method-energyconstraints-__init__)

##### `check_all(self, kinetic, potential)`

Check energy constraints.

[View full source →](#method-energyconstraints-check_all)

---

### `ConstraintChecker`

Unified constraint checker for simulation safety.

#### Source Code

```{literalinclude} ../../../src/simulation/safety/constraints.py
:language: python
:pyobject: ConstraintChecker
:linenos:
```

#### Methods (4)

##### `__init__(self, state_constraints, control_constraints, energy_constraints)`

Initialize constraint checker.

[View full source →](#method-constraintchecker-__init__)

##### `check_state(self, state)`

Check state constraints.

[View full source →](#method-constraintchecker-check_state)

##### `check_control(self, control, dt)`

Check control constraints.

[View full source →](#method-constraintchecker-check_control)

##### `check_energy(self, kinetic, potential)`

Check energy constraints.

[View full source →](#method-constraintchecker-check_energy)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from abc import ABC, abstractmethod`
- `from typing import Any, Dict, Optional, Tuple`
- `import numpy as np`
