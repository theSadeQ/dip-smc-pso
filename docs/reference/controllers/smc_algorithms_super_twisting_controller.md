# controllers.smc.algorithms.super_twisting.controller

**Source:** `src\controllers\smc\algorithms\super_twisting\controller.py`

## Module Overview

Modular Super-Twisting SMC Controller.

Implements Super-Twisting Sliding Mode Control using composed components:
- LinearSlidingSurface: Surface computation
- SuperTwistingAlgorithm: Second-order sliding mode control
- SwitchingFunction: Smooth chattering reduction

Provides finite-time convergence with chattering reduction through
second-order sliding mode dynamics.


## Mathematical Foundation

### Super-Twisting Algorithm (STA)

Second-order sliding mode control with continuous control signal:

```{math}
\begin{align}
u &= -K_1 |s|^{1/2} \text{sign}(s) + u_1 \\
\dot{u}_1 &= -K_2 \text{sign}(s)
\end{align}
```

### Finite-Time Convergence

STA ensures $s = \dot{s} = 0$ in finite time with:

```{math}
K_1 > 0, \quad K_2 > \frac{L}{2}
```

Where $L$ is the Lipschitz constant of disturbances.

### Chattering-Free Property

Continuous control eliminates chattering while maintaining finite-time convergence.

**See:** {doc}`../../../mathematical_foundations/smc_complete_theory`


## Complete Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/super_twisting/controller.py
:language: python
:linenos:
```

---

## Classes

### `ModularSuperTwistingSMC`

Modular Super-Twisting SMC using composition of focused components.

Super-Twisting control law:
u = u₁ + u₂
u₁ = -K₁|s|^α sign(s)
u₂ = -K₂ ∫sign(s)dt

Provides finite-time convergence when K₁ > K₂ > 0.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/super_twisting/controller.py
:language: python
:pyobject: ModularSuperTwistingSMC
:linenos:
```

#### Methods (16)

##### `__init__(self, config, dynamics)`

Initialize modular Super-Twisting SMC.

[View full source →](#method-modularsupertwistingsmc-__init__)

##### `compute_control(self, state, state_vars, history, dt)`

Compute Super-Twisting SMC control law.

[View full source →](#method-modularsupertwistingsmc-compute_control)

##### `_estimate_surface_derivative(self, state, current_surface)`

Estimate surface derivative using finite differences.

[View full source →](#method-modularsupertwistingsmc-_estimate_surface_derivative)

##### `_create_control_result(self, u_final, surface_value, surface_derivative, twisting_result, damping_control, u_before_sat)`

Create structured control result.

[View full source →](#method-modularsupertwistingsmc-_create_control_result)

##### `_create_error_result(self, error_msg)`

Create error result with safe defaults.

[View full source →](#method-modularsupertwistingsmc-_create_error_result)

##### `_is_anti_windup_active(self)`

Check if anti-windup is currently active.

[View full source →](#method-modularsupertwistingsmc-_is_anti_windup_active)

##### `gains(self)`

Return controller gains [K1, K2, k1, k2, λ1, λ2].

[View full source →](#method-modularsupertwistingsmc-gains)

##### `validate_gains(self, gains_b)`

Vectorized feasibility check for super‑twisting SMC gains.

[View full source →](#method-modularsupertwistingsmc-validate_gains)

##### `get_twisting_gains(self)`

Get Super-Twisting gains (K1, K2).

[View full source →](#method-modularsupertwistingsmc-get_twisting_gains)

##### `set_twisting_gains(self, K1, K2)`

Update Super-Twisting gains.

[View full source →](#method-modularsupertwistingsmc-set_twisting_gains)

##### `reset_controller(self)`

Reset controller to initial state.

[View full source →](#method-modularsupertwistingsmc-reset_controller)

##### `reset(self)`

Reset controller state (interface compliance).

[View full source →](#method-modularsupertwistingsmc-reset)

##### `get_stability_analysis(self)`

Get comprehensive stability analysis.

[View full source →](#method-modularsupertwistingsmc-get_stability_analysis)

##### `tune_gains(self, K1, K2, boundary_layer)`

Tune controller parameters during runtime.

[View full source →](#method-modularsupertwistingsmc-tune_gains)

##### `get_parameters(self)`

Get all controller parameters.

[View full source →](#method-modularsupertwistingsmc-get_parameters)

##### `get_convergence_estimate(self, current_surface)`

Estimate convergence properties.

[View full source →](#method-modularsupertwistingsmc-get_convergence_estimate)

---

### `SuperTwistingSMC`

Backward-compatible facade for the modular Super-Twisting SMC.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/super_twisting/controller.py
:language: python
:pyobject: SuperTwistingSMC
:linenos:
```

#### Methods (6)

##### `__init__(self, gains, dt, max_force)`

Initialize Super-Twisting SMC with legacy interface.

[View full source →](#method-supertwistingsmc-__init__)

##### `compute_control(self, state, state_vars, history)`

Compute control (delegates to modular controller).

[View full source →](#method-supertwistingsmc-compute_control)

##### `gains(self)`

Return controller gains.

[View full source →](#method-supertwistingsmc-gains)

##### `get_twisting_gains(self)`

Get Super-Twisting gains.

[View full source →](#method-supertwistingsmc-get_twisting_gains)

##### `reset_controller(self)`

Reset controller state.

[View full source →](#method-supertwistingsmc-reset_controller)

##### `get_parameters(self)`

Get controller parameters.

[View full source →](#method-supertwistingsmc-get_parameters)

---

## Dependencies

This module imports:

- `from typing import Dict, List, Union, Optional, Any`
- `import numpy as np`
- `import logging`
- `from ...core.sliding_surface import LinearSlidingSurface`
- `from ...core.switching_functions import SwitchingFunction`
- `from .twisting_algorithm import SuperTwistingAlgorithm`
- `from .config import SuperTwistingSMCConfig`
