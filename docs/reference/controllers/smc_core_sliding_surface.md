# controllers.smc.core.sliding_surface

**Source:** `src\controllers\smc\core\sliding_surface.py`

## Module Overview

Sliding Surface Calculations for SMC Controllers.

Provides unified sliding surface computation that can be shared across all SMC types.
Implements both linear and nonlinear sliding surface formulations with proper
mathematical foundations.

Mathematical Background:
- Linear sliding surface: s = c₁e₁ + c₂e₂ + λ₁ė₁ + λ₂ė₂
- Where e₁, e₂ are tracking errors and ė₁, ė₂ are error derivatives
- Coefficients c₁, c₂, λ₁, λ₂ must be positive for stability (Hurwitz requirement)

## Complete Source Code

```{literalinclude} ../../../src/controllers/smc/core/sliding_surface.py
:language: python
:linenos:
```

---

## Classes

### `SlidingSurface`

**Inherits from:** `ABC`

Abstract base class for sliding surface calculations.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/core/sliding_surface.py
:language: python
:pyobject: SlidingSurface
:linenos:
```

#### Methods (4)

##### `__init__(self, gains)`

[View full source →](#method-slidingsurface-__init__)

##### `_validate_gains(self)`

Validate gains for this specific sliding surface type.

[View full source →](#method-slidingsurface-_validate_gains)

##### `compute(self, state)`

Compute sliding surface value for given state.

[View full source →](#method-slidingsurface-compute)

##### `compute_derivative(self, state, state_dot)`

Compute sliding surface derivative ds/dt.

[View full source →](#method-slidingsurface-compute_derivative)

---

### `LinearSlidingSurface`

**Inherits from:** `SlidingSurface`

Linear sliding surface for conventional SMC.

Implements: s = λ₁ė₁ + c₁e₁ + λ₂ė₂ + c₂e₂

For double-inverted pendulum:
- e₁ = θ₁ (joint 1 angle error)
- e₂ = θ₂ (joint 2 angle error)
- ė₁ = θ̇₁ (joint 1 velocity error)
- ė₂ = θ̇₂ (joint 2 velocity error)

#### Source Code

```{literalinclude} ../../../src/controllers/smc/core/sliding_surface.py
:language: python
:pyobject: LinearSlidingSurface
:linenos:
```

#### Methods (6)

##### `__init__(self, gains)`

Initialize linear sliding surface.

[View full source →](#method-linearslidingsurface-__init__)

##### `_validate_gains(self)`

Validate that surface gains satisfy stability requirements.

[View full source →](#method-linearslidingsurface-_validate_gains)

##### `compute(self, state)`

Compute linear sliding surface value.

[View full source →](#method-linearslidingsurface-compute)

##### `compute_surface(self, state)`

Compatibility method for test interface - alias for compute().

[View full source →](#method-linearslidingsurface-compute_surface)

##### `compute_derivative(self, state, state_dot)`

Compute sliding surface derivative ds/dt.

[View full source →](#method-linearslidingsurface-compute_derivative)

##### `get_coefficients(self)`

Return surface coefficients for analysis.

[View full source →](#method-linearslidingsurface-get_coefficients)

---

### `HigherOrderSlidingSurface`

**Inherits from:** `SlidingSurface`

Higher-order sliding surface for Super-Twisting and advanced SMC.

Implements surfaces that include higher-order derivatives for
finite-time convergence and better disturbance rejection.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/core/sliding_surface.py
:language: python
:pyobject: HigherOrderSlidingSurface
:linenos:
```

#### Methods (4)

##### `__init__(self, gains, order)`

Initialize higher-order sliding surface.

[View full source →](#method-higherorderslidingsurface-__init__)

##### `_validate_gains(self)`

Validate gains for higher-order stability.

[View full source →](#method-higherorderslidingsurface-_validate_gains)

##### `compute(self, state)`

Compute higher-order sliding surface (simplified implementation).

[View full source →](#method-higherorderslidingsurface-compute)

##### `compute_derivative(self, state, state_dot)`

Compute higher-order surface derivative.

[View full source →](#method-higherorderslidingsurface-compute_derivative)

---

## Functions

### `create_sliding_surface(surface_type, gains)`

Factory function for creating sliding surfaces.

Args:
    surface_type: "linear" or "higher_order"
    gains: Gain vector

Returns:
    Appropriate sliding surface instance

#### Source Code

```{literalinclude} ../../../src/controllers/smc/core/sliding_surface.py
:language: python
:pyobject: create_sliding_surface
:linenos:
```

---

## Dependencies

This module imports:

- `from typing import List, Optional, Union, Sequence`
- `import numpy as np`
- `from abc import ABC, abstractmethod`
