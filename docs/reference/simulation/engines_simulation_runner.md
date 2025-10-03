# simulation.engines.simulation_runner

**Source:** `src\simulation\engines\simulation_runner.py`

## Module Overview

Simulation step router.

This module dispatches between full and low‑rank dynamics implementations
based on ``config.simulation.use_full_dynamics``.  It exposes a unified
``step(x, u, dt)`` function which calls either ``src.plant.models.dip_full.step``
or ``src.plant.models.dip_lowrank.step`` depending on the configuration.

If the full dynamics module cannot be imported, a RuntimeError with a
specific message is raised.  Tests match the message text exactly.

## Complete Source Code

```{literalinclude} ../../../src/simulation/engines/simulation_runner.py
:language: python
:linenos:
```

---

## Classes

### `SimulationRunner`

Object-oriented wrapper around the run_simulation function.

This class provides compatibility with test cases that expect a
SimulationRunner class interface while maintaining the functional API.

#### Source Code

```{literalinclude} ../../../src/simulation/engines/simulation_runner.py
:language: python
:pyobject: SimulationRunner
:linenos:
```

#### Methods (2)

##### `__init__(self, dynamics_model, dt, max_time)`

Initialize simulation runner.

[View full source →](#method-simulationrunner-__init__)

##### `run_simulation(self, initial_state, controller, reference)`

Run simulation using the functional API.

[View full source →](#method-simulationrunner-run_simulation)

---

## Functions

### `_load_full_step()`

Attempt to load the full dynamics ``step`` function.

Returns
-------
callable
    The ``step(x, u, dt)`` function from the full dynamics module.

Raises
------
RuntimeError
    If the module cannot be imported or does not define ``step``.

#### Source Code

```{literalinclude} ../../../src/simulation/engines/simulation_runner.py
:language: python
:pyobject: _load_full_step
:linenos:
```

---

### `_load_lowrank_step()`

Load the low‑rank dynamics ``step`` function.

Returns
-------
callable
    The low‑rank ``step(x, u, dt)`` function.

#### Source Code

```{literalinclude} ../../../src/simulation/engines/simulation_runner.py
:language: python
:pyobject: _load_lowrank_step
:linenos:
```

---

### `get_step_fn()`

Return the appropriate step function based on the configuration flag.

Returns
-------
callable
    Either ``src.plant.models.dip_full.step`` or ``src.plant.models.dip_lowrank.step``.

#### Source Code

```{literalinclude} ../../../src/simulation/engines/simulation_runner.py
:language: python
:pyobject: get_step_fn
:linenos:
```

---

### `step(x, u, dt)`

Unified simulation step entry point.

Parameters
----------
x : array-like
    Current state.
u : array-like
    Control input(s).
dt : float
    Timestep.

Returns
-------
array-like
    Next state computed by the selected dynamics implementation.

#### Source Code

```{literalinclude} ../../../src/simulation/engines/simulation_runner.py
:language: python
:pyobject: step
:linenos:
```

---

### `run_simulation()`

Simulate a single controller trajectory using an explicit Euler method.

The runner integrates the provided ``dynamics_model`` forward in time under
the control law defined by ``controller``.  It produces uniformly spaced
timestamps, a state trajectory and the applied control sequence.  If the
dynamics return NaN/Inf values or raise an exception at any step, the
simulation halts immediately and the outputs are truncated to include only
the steps executed.  Control inputs can be saturated via the ``u_max``
parameter or by querying ``controller.max_force`` when ``u_max`` is not
provided.  Stateful controllers may expose optional hooks
``initialize_state`` and ``initialize_history``; these are called once at
the beginning of the simulation.  A ``compute_control`` method, if
available, is preferred over ``__call__`` for computing the control.  The
runner also supports a simple latency monitor: if computing the control
exceeds the nominal period ``dt`` on any step and a ``fallback_controller``
is provided, subsequent control inputs are drawn from the fallback.

Parameters
----------
controller : Any
    The control object.  Must implement ``__call__(t, x) -> float`` or
    ``compute_control(x, state_vars, history)``.  Optional hooks
    ``initialize_state`` and ``initialize_history`` may be defined to
    initialise controller state.
dynamics_model : Any
    Object providing a ``step(state, u, dt)`` method that advances the
    state forward in time.  Must accept a state vector and scalar input
    ``u``.
sim_time : float
    Total simulation horizon in seconds.  The integration runs until
    the largest multiple of ``dt`` not exceeding ``sim_time``.  A value
    less than or equal to zero produces no integration steps.
dt : float
    Integration timestep (seconds).  Must be strictly positive.
initial_state : array-like
    Initial state vector.  Converted to ``float`` and flattened.  The
    length of the state vector defines the dimensionality of the system.
u_max : float, optional
    Saturation limit for the control input.  When provided, control
    commands are clipped to the interval ``[-u_max, u_max]``.  If omitted
    and the controller exposes ``max_force``, that value is used instead.
seed : int, optional
    Deprecated.  Present for backward compatibility; use ``rng`` to
    control randomness when required.  When both ``seed`` and ``rng`` are
    provided, ``rng`` takes precedence.
rng : numpy.random.Generator, optional
    Random number generator for controllers that rely on sampling.  If
    provided, it is passed unchanged to the controller; otherwise a local
    generator may be created when ``seed`` is supplied.
latency_margin : float, optional
    Unused placeholder for future latency control.  Accepts any value
    without effect.
fallback_controller : callable, optional
    Function ``fallback_controller(t, x) -> float`` invoked to compute
    control after a deadline miss.  When a control call exceeds ``dt`` in
    duration, the fallback controller is used for all subsequent steps.
**_kwargs : dict
    Additional keyword arguments are ignored.  They are accepted to
    preserve backward compatibility with earlier versions of this API.

Returns
-------
t_arr : numpy.ndarray
    1D array of time points including the initial time at index 0.  The
    final element equals ``n_steps * dt`` where ``n_steps = int(round(sim_time / dt))``.
x_arr : numpy.ndarray
    2D array of shape ``(len(t_arr), D)`` containing the state trajectory.
u_arr : numpy.ndarray
    1D array of shape ``(len(t_arr) - 1,)`` containing the applied control
    sequence.  Empty if no integration steps were executed.

#### Source Code

```{literalinclude} ../../../src/simulation/engines/simulation_runner.py
:language: python
:pyobject: run_simulation
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from importlib import import_module`
- `import time`
- `from typing import Any, Callable, Optional, Tuple`
- `import numpy as np`
