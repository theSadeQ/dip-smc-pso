# controllers.smc.algorithms.adaptive.controller

**Source:** `src\controllers\smc\algorithms\adaptive\controller.py`

## Module Overview

Modular Adaptive SMC Controller.

Implements Adaptive Sliding Mode Control using composed components:
- LinearSlidingSurface: Surface computation
- AdaptationLaw: Online gain adjustment
- UncertaintyEstimator: Disturbance bound estimation
- SwitchingFunction: Smooth chattering reduction

Replaces the monolithic 427-line controller with composition of focused modules.


## Mathematical Foundation

### Adaptive Sliding Mode Control

Adaptive SMC handles system uncertainties through online gain adaptation:

```{math}
\dot{K} = \gamma |s| - \sigma(K - K_0)
```

Where:
- $\gamma > 0$: Adaptation rate
- $\sigma > 0$: Leakage term preventing unbounded growth
- $K_0$: Initial gain estimate

### Stability with Adaptation

Modified Lyapunov function:

```{math}
V(s, \tilde{K}) = \frac{1}{2}s^2 + \frac{1}{2\gamma}\tilde{K}^2
```

Where $\tilde{K} = K - K^*$ is the gain error. The derivative becomes:

```{math}
\dot{V} = -K^*|s| - \sigma \tilde{K}^2 \leq 0
```

Ensuring asymptotic stability even with unknown uncertainty bounds.

**See:** {doc}`../../../mathematical_foundations/smc_complete_theory` for adaptation law derivation.


## Complete Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/adaptive/controller.py
:language: python
:linenos:
```

---

## Classes

### `ModularAdaptiveSMC`

Modular Adaptive SMC using composition of focused components.

Adaptive SMC law: u = -K(t) * sign(s)
Where K(t) adapts online: K̇ = γ|s| - σK

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/adaptive/controller.py
:language: python
:pyobject: ModularAdaptiveSMC
:linenos:
```

#### Methods (12)

##### `__init__(self, config, dynamics)`

Initialize modular adaptive SMC.

[View full source →](#method-modularadaptivesmc-__init__)

##### `compute_control(self, state, state_vars, history, dt)`

Compute adaptive SMC control law.

[View full source →](#method-modularadaptivesmc-compute_control)

##### `_estimate_surface_derivative(self, state, current_surface)`

Estimate surface derivative using finite differences.

[View full source →](#method-modularadaptivesmc-_estimate_surface_derivative)

##### `_create_control_result(self, u_final, surface_value, surface_derivative, adaptive_gain, uncertainty_bound, switching_output, u_before_sat)`

Create structured control result.

[View full source →](#method-modularadaptivesmc-_create_control_result)

##### `_create_error_result(self, error_msg)`

Create error result with safe defaults.

[View full source →](#method-modularadaptivesmc-_create_error_result)

##### `gains(self)`

Return controller gains (static configuration gains only).

[View full source →](#method-modularadaptivesmc-gains)

##### `get_adaptive_gain(self)`

Get current adaptive gain value.

[View full source →](#method-modularadaptivesmc-get_adaptive_gain)

##### `reset(self)`

Reset controller to initial state (standard interface).

[View full source →](#method-modularadaptivesmc-reset)

##### `reset_adaptation(self, initial_gain)`

Reset adaptive components to initial state.

[View full source →](#method-modularadaptivesmc-reset_adaptation)

##### `get_adaptation_analysis(self)`

Get comprehensive adaptation analysis.

[View full source →](#method-modularadaptivesmc-get_adaptation_analysis)

##### `tune_adaptation_parameters(self, gamma, sigma, rate_limit)`

Tune adaptation parameters during runtime.

[View full source →](#method-modularadaptivesmc-tune_adaptation_parameters)

##### `get_parameters(self)`

Get all controller parameters.

[View full source →](#method-modularadaptivesmc-get_parameters)

---

### `AdaptiveSMC`

Backward-compatible facade for the modular Adaptive SMC.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/adaptive/controller.py
:language: python
:pyobject: AdaptiveSMC
:linenos:
```

#### Methods (7)

##### `__init__(self, gains, dt, max_force)`

Initialize Adaptive SMC with legacy interface.

[View full source →](#method-adaptivesmc-__init__)

##### `compute_control(self, state, state_vars, history)`

Compute control (delegates to modular controller).

[View full source →](#method-adaptivesmc-compute_control)

##### `gains(self)`

Return controller gains.

[View full source →](#method-adaptivesmc-gains)

##### `get_adaptive_gain(self)`

Get current adaptive gain.

[View full source →](#method-adaptivesmc-get_adaptive_gain)

##### `reset(self)`

Reset controller to initial state.

[View full source →](#method-adaptivesmc-reset)

##### `reset_adaptation(self)`

Reset adaptation state.

[View full source →](#method-adaptivesmc-reset_adaptation)

##### `get_parameters(self)`

Get controller parameters.

[View full source →](#method-adaptivesmc-get_parameters)

---

## Dependencies

This module imports:

- `from typing import Dict, List, Union, Optional, Any`
- `import numpy as np`
- `import logging`
- `from ...core.sliding_surface import LinearSlidingSurface`
- `from ...core.switching_functions import SwitchingFunction`
- `from .adaptation_law import AdaptationLaw`
- `from .parameter_estimation import UncertaintyEstimator`
- `from .config import AdaptiveSMCConfig`
