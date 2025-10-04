# simulation.integrators.factory

**Source:** `src\simulation\integrators\factory.py`

## Module Overview

Integrator Factory for creating numerical integration instances.

This module provides a factory pattern for instantiating different types
of numerical integrators with proper configuration and parameter management.

## Complete Source Code

```{literalinclude} ../../../src/simulation/integrators/factory.py
:language: python
:linenos:
```

---

## Classes

### `IntegratorFactory`

Factory for creating numerical integrator instances.

Provides centralized creation and management of integrators
with validation and consistency checking.

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/factory.py
:language: python
:pyobject: IntegratorFactory
:linenos:
```

#### Methods (5)

##### `create_integrator(cls, integrator_type, dt)`

Create an integrator instance of the specified type.

[View full source →](#method-integratorfactory-create_integrator)

##### `list_available_integrators(cls)`

Get list of available integrator types.

[View full source →](#method-integratorfactory-list_available_integrators)

##### `get_integrator_info(cls, integrator_type)`

Get information about an integrator type.

[View full source →](#method-integratorfactory-get_integrator_info)

##### `register_integrator(cls, name, integrator_class)`

Register a custom integrator class.

[View full source →](#method-integratorfactory-register_integrator)

##### `create_default_integrator(cls, dt)`

Create a default integrator instance.

[View full source →](#method-integratorfactory-create_default_integrator)

---

## Functions

### `create_integrator(integrator_type, dt)`

Create integrator instance (convenience function).

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/factory.py
:language: python
:pyobject: create_integrator
:linenos:
```

---

### `get_available_integrators()`

Get available integrator types (convenience function).

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/factory.py
:language: python
:pyobject: get_available_integrators
:linenos:
```

---

## Dependencies

This module imports:

- `from typing import Dict, Type, Any, Optional, Union`
- `import logging`
- `from .base import BaseIntegrator`
- `from .fixed_step.euler import ForwardEuler, BackwardEuler`
- `from .fixed_step.runge_kutta import RungeKutta4, RungeKutta2`
- `from .adaptive.runge_kutta import AdaptiveRungeKutta, DormandPrince45`
- `from .discrete.zero_order_hold import ZeroOrderHold`
