# controllers.smc.algorithms.super_twisting.twisting_algorithm

**Source:** `src\controllers\smc\algorithms\super_twisting\twisting_algorithm.py`

## Module Overview

Super-Twisting Algorithm Implementation.

Implements the core Super-Twisting sliding mode algorithm for finite-time convergence.
The algorithm provides second-order sliding mode control with chattering reduction.

Mathematical Background:
- Control law: u = u₁ + u₂
- u₁ = -K₁|s|^α sign(s)
- u₂ = -K₂ ∫sign(s)dt
- Stability: K₁ > K₂ > 0 for finite-time convergence

## Complete Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/super_twisting/twisting_algorithm.py
:language: python
:linenos:
```

---

## Classes

### `SuperTwistingAlgorithm`

Core Super-Twisting sliding mode algorithm.

Implements second-order sliding mode control with finite-time convergence:
- Continuous control component: u₁ = -K₁|s|^α sign(s)
- Integral component: u₂ = -K₂ ∫sign(s)dt

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/super_twisting/twisting_algorithm.py
:language: python
:pyobject: SuperTwistingAlgorithm
:linenos:
```

#### Methods (11)

##### `__init__(self, K1, K2, alpha, anti_windup_limit, regularization)`

Initialize Super-Twisting algorithm.

[View full source →](#method-supertwistingalgorithm-__init__)

##### `compute_control(self, surface_value, dt, switching_function, boundary_layer)`

Compute Super-Twisting control law.

[View full source →](#method-supertwistingalgorithm-compute_control)

##### `_compute_switching_function(self, s, method, epsilon)`

Compute switching function sign(s) with smooth approximation.

[View full source →](#method-supertwistingalgorithm-_compute_switching_function)

##### `reset_state(self)`

Reset algorithm internal state.

[View full source →](#method-supertwistingalgorithm-reset_state)

##### `set_gains(self, K1, K2)`

Update twisting gains.

[View full source →](#method-supertwistingalgorithm-set_gains)

##### `get_gains(self)`

Get current twisting gains (K1, K2).

[View full source →](#method-supertwistingalgorithm-get_gains)

##### `check_stability_condition(self)`

Check if current gains satisfy stability condition.

[View full source →](#method-supertwistingalgorithm-check_stability_condition)

##### `estimate_convergence_time(self, initial_surface)`

Estimate finite-time convergence time.

[View full source →](#method-supertwistingalgorithm-estimate_convergence_time)

##### `analyze_performance(self, surface_history)`

Analyze Super-Twisting performance from surface history.

[View full source →](#method-supertwistingalgorithm-analyze_performance)

##### `get_lyapunov_function(self, surface_value, surface_derivative)`

Compute Lyapunov function for stability analysis.

[View full source →](#method-supertwistingalgorithm-get_lyapunov_function)

##### `get_state_dict(self)`

Get current algorithm state for logging/debugging.

[View full source →](#method-supertwistingalgorithm-get_state_dict)

---

## Dependencies

This module imports:

- `from typing import Optional, Dict, Any`
- `import numpy as np`
- `import math`
