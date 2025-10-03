# controllers.smc.algorithms.adaptive.adaptation_law

**Source:** `src\controllers\smc\algorithms\adaptive\adaptation_law.py`

## Module Overview

Adaptive Gain Update Laws for Adaptive SMC.

Implements online gain adaptation algorithms based on sliding mode theory.
The adaptation law adjusts switching gain K(t) to handle unknown uncertainties.

Mathematical Background:
- Adaptation law: K̇ = γ|s| - σK (with leakage)
- Lyapunov stability: V̇ = sṡ + (K̃/γ)K̇ ≤ 0
- Bounded adaptation: K_min ≤ K(t) ≤ K_max

## Complete Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/adaptive/adaptation_law.py
:language: python
:linenos:
```

---

## Classes

### `AdaptationLaw`

Online gain adaptation for Adaptive SMC.

Implements adaptive laws that adjust switching gains based on
sliding surface behavior to handle uncertain disturbances.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/adaptive/adaptation_law.py
:language: python
:pyobject: AdaptationLaw
:linenos:
```

#### Methods (9)

##### `__init__(self, adaptation_rate, uncertainty_bound, leak_rate, rate_limit, bounds, dead_zone)`

Initialize adaptation law.

[View full source →](#method-adaptationlaw-__init__)

##### `update_gain(self, surface_value, dt, uncertainty_estimate)`

Update adaptive gain using adaptation law.

[View full source →](#method-adaptationlaw-update_gain)

##### `get_current_gain(self)`

Get current adaptive gain value.

[View full source →](#method-adaptationlaw-get_current_gain)

##### `reset_gain(self, initial_gain)`

Reset adaptive gain to initial value.

[View full source →](#method-adaptationlaw-reset_gain)

##### `is_adaptation_active(self, surface_value)`

Check if adaptation is currently active.

[View full source →](#method-adaptationlaw-is_adaptation_active)

##### `get_adaptation_rate(self, surface_value)`

Get current adaptation rate K̇.

[View full source →](#method-adaptationlaw-get_adaptation_rate)

##### `analyze_adaptation_performance(self)`

Analyze adaptation performance from history.

[View full source →](#method-adaptationlaw-analyze_adaptation_performance)

##### `set_adaptation_parameters(self, gamma, sigma, rate_limit)`

Update adaptation parameters during runtime.

[View full source →](#method-adaptationlaw-set_adaptation_parameters)

##### `get_lyapunov_derivative(self, surface_value, surface_derivative)`

Compute Lyapunov function derivative for stability analysis.

[View full source →](#method-adaptationlaw-get_lyapunov_derivative)

---

### `ModifiedAdaptationLaw`

**Inherits from:** `AdaptationLaw`

Modified adaptation law with additional robustness features.

Includes projection operator and improved stability properties.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/adaptive/adaptation_law.py
:language: python
:pyobject: ModifiedAdaptationLaw
:linenos:
```

#### Methods (3)

##### `__init__(self)`

Initialize modified adaptation law.

[View full source →](#method-modifiedadaptationlaw-__init__)

##### `update_gain(self, surface_value, dt, uncertainty_estimate)`

Update gain with projection operator.

[View full source →](#method-modifiedadaptationlaw-update_gain)

##### `_is_projection_active(self, K_dot)`

Check if projection operator is currently active.

[View full source →](#method-modifiedadaptationlaw-_is_projection_active)

---

## Dependencies

This module imports:

- `from typing import Optional, Union`
- `import numpy as np`
