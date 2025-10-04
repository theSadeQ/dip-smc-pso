# controllers.smc.algorithms.classical.controller

**Source:** `src\controllers\smc\algorithms\classical\controller.py`

## Module Overview

Modular Classical SMC Controller.

Clean implementation using focused components:
- SlidingSurface: Surface computation
- EquivalentControl: Model-based feedforward
- BoundaryLayer: Chattering reduction
- Configuration: Type-safe parameters

Replaces the monolithic 458-line controller with composition of 50-100 line modules.

## Complete Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/classical/controller.py
:language: python
:linenos:
```

---

## Classes

### `ModularClassicalSMC`

Modular Classical SMC controller using composition of focused components.

Components:
- Sliding surface: Computes s = λ₁ė₁ + c₁e₁ + λ₂ė₂ + c₂e₂
- Equivalent control: Model-based u_eq = -(LM⁻¹B)⁻¹LM⁻¹F
- Boundary layer: Continuous switching with chattering reduction

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/classical/controller.py
:language: python
:pyobject: ModularClassicalSMC
:linenos:
```

#### Methods (9)

##### `__init__(self, config)`

Initialize modular classical SMC.

[View full source →](#method-modularclassicalsmc-__init__)

##### `compute_control(self, state, state_vars, history)`

Compute classical SMC control law.

[View full source →](#method-modularclassicalsmc-compute_control)

##### `_estimate_surface_derivative(self, state)`

Estimate surface derivative for derivative control.

[View full source →](#method-modularclassicalsmc-_estimate_surface_derivative)

##### `_create_control_result(self, u_final, surface_value, surface_derivative, u_eq, u_switch, u_deriv, u_total)`

Create structured control result.

[View full source →](#method-modularclassicalsmc-_create_control_result)

##### `_create_error_result(self, error_msg)`

Create error result with safe defaults.

[View full source →](#method-modularclassicalsmc-_create_error_result)

##### `gains(self)`

Return controller gains for interface compatibility.

[View full source →](#method-modularclassicalsmc-gains)

##### `reset(self)`

Reset controller to initial state.

[View full source →](#method-modularclassicalsmc-reset)

##### `get_parameters(self)`

Get all controller parameters.

[View full source →](#method-modularclassicalsmc-get_parameters)

##### `analyze_performance(self, surface_history, control_history, dt)`

Analyze controller performance.

[View full source →](#method-modularclassicalsmc-analyze_performance)

---

### `ClassicalSMC`

Backward-compatible facade for the modular Classical SMC.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/classical/controller.py
:language: python
:pyobject: ClassicalSMC
:linenos:
```

#### Methods (5)

##### `__init__(self, gains, max_force, boundary_layer, dynamics_model)`

Initialize Classical SMC with legacy interface.

[View full source →](#method-classicalsmc-__init__)

##### `compute_control(self, state, state_vars, history)`

Compute control (delegates to modular controller).

[View full source →](#method-classicalsmc-compute_control)

##### `gains(self)`

Return controller gains.

[View full source →](#method-classicalsmc-gains)

##### `reset(self)`

Reset controller to initial state.

[View full source →](#method-classicalsmc-reset)

##### `get_parameters(self)`

Get controller parameters.

[View full source →](#method-classicalsmc-get_parameters)

---

## Dependencies

This module imports:

- `from typing import Dict, List, Union, Optional, Any`
- `import numpy as np`
- `import logging`
- `from ...core.sliding_surface import LinearSlidingSurface`
- `from ...core.equivalent_control import EquivalentControl`
- `from .boundary_layer import BoundaryLayer`
- `from .config import ClassicalSMCConfig`
