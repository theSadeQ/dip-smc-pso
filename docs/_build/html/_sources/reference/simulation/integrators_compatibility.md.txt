# simulation.integrators.compatibility

**Source:** `src\simulation\integrators\compatibility.py`

## Module Overview

Integrator compatibility wrapper for simulation engine integration.

This module provides compatibility wrappers to bridge the interface mismatch between
simulation engines that expect dynamics_model.step(x, u, dt) and integrators that
expect dynamics_fn(t, x, u) -> dx/dt. It ensures seamless integration of adaptive
and fixed-step integrators with the simulation framework.

## Complete Source Code

```{literalinclude} ../../../src/simulation/integrators/compatibility.py
:language: python
:linenos:
```

---

## Classes

### `DynamicsCompatibilityWrapper`

Wrapper to make integrators compatible with simulation dynamics interface.

Converts between:
- Simulation interface: dynamics_model.step(state, control, dt) -> next_state
- Integrator interface: dynamics_fn(time, state, control) -> state_derivative

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/compatibility.py
:language: python
:pyobject: DynamicsCompatibilityWrapper
:linenos:
```

#### Methods (3)

##### `__init__(self, integrator, dynamics_fn)`

Initialize compatibility wrapper.

[View full source →](#method-dynamicscompatibilitywrapper-__init__)

##### `step(self, state, control, dt)`

Step the dynamics using the wrapped integrator.

[View full source →](#method-dynamicscompatibilitywrapper-step)

##### `reset_time(self, t)`

Reset the internal time counter.

[View full source →](#method-dynamicscompatibilitywrapper-reset_time)

---

### `LegacyDynamicsWrapper`

Wrapper to adapt legacy dynamics models to integrator interface.

Converts from:
- Legacy interface: dynamics.step(state, control, dt) -> next_state
To:
- Integrator interface: dynamics_fn(t, x, u) -> dx/dt

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/compatibility.py
:language: python
:pyobject: LegacyDynamicsWrapper
:linenos:
```

#### Methods (2)

##### `__init__(self, legacy_dynamics)`

Initialize legacy wrapper.

[View full source →](#method-legacydynamicswrapper-__init__)

##### `__call__(self, t, state, control)`

Convert legacy step to derivative function.

[View full source →](#method-legacydynamicswrapper-__call__)

---

### `IntegratorSafetyWrapper`

Safety wrapper for integrators to handle edge cases and errors gracefully.

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/compatibility.py
:language: python
:pyobject: IntegratorSafetyWrapper
:linenos:
```

#### Methods (4)

##### `__init__(self, base_integrator, fallback_integrator)`

Initialize safety wrapper.

[View full source →](#method-integratorsafetywrapper-__init__)

##### `integrate(self, dynamics_fn, state, control, dt)`

Safely integrate with automatic fallback on failure.

[View full source →](#method-integratorsafetywrapper-integrate)

##### `_safe_fallback_integrate(self, dynamics_fn, state, control, dt)`

Safely integrate using fallback method.

[View full source →](#method-integratorsafetywrapper-_safe_fallback_integrate)

##### `reset(self)`

Reset the safety wrapper state.

[View full source →](#method-integratorsafetywrapper-reset)

---

## Functions

### `create_compatible_dynamics(integrator_type, dynamics_fn, legacy_dynamics)`

Create a dynamics model compatible with simulation engines.

Parameters
----------
integrator_type : str
    Type of integrator ('euler', 'rk4', 'rk45', 'dopri45')
dynamics_fn : callable, optional
    Dynamics function with signature (t, x, u) -> dx/dt
legacy_dynamics : object, optional
    Legacy dynamics with step(x, u, dt) method
**integrator_kwargs
    Additional arguments for integrator initialization

Returns
-------
DynamicsCompatibilityWrapper
    Wrapped dynamics model compatible with simulation engines

Examples
--------
>>> def pendulum_dynamics(t, x, u):
...     return np.array([x[1], -np.sin(x[0]) - 0.1*x[1] + u])
>>>
>>> dynamics = create_compatible_dynamics('rk4', pendulum_dynamics)
>>> next_state = dynamics.step(np.array([0.1, 0.0]), 0.5, 0.01)

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/compatibility.py
:language: python
:pyobject: create_compatible_dynamics
:linenos:
```

---

### `create_safe_integrator(integrator_type)`

Create a safety-wrapped integrator.

Parameters
----------
integrator_type : str
    Type of integrator
**kwargs
    Integrator parameters

Returns
-------
IntegratorSafetyWrapper
    Safety-wrapped integrator

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/compatibility.py
:language: python
:pyobject: create_safe_integrator
:linenos:
```

---

### `create_robust_euler_dynamics(dynamics_fn)`

Create robust Euler-integrated dynamics.

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/compatibility.py
:language: python
:pyobject: create_robust_euler_dynamics
:linenos:
```

---

### `create_robust_rk4_dynamics(dynamics_fn)`

Create robust RK4-integrated dynamics.

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/compatibility.py
:language: python
:pyobject: create_robust_rk4_dynamics
:linenos:
```

---

### `create_robust_adaptive_dynamics(dynamics_fn, rtol, atol)`

Create robust adaptive-integrated dynamics.

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/compatibility.py
:language: python
:pyobject: create_robust_adaptive_dynamics
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Callable, Any, Optional, Union`
- `import numpy as np`
- `from .base import BaseIntegrator`
- `from .fixed_step.euler import ForwardEuler`
- `from .fixed_step.runge_kutta import RungeKutta4`
- `from .adaptive.runge_kutta import DormandPrince45`
