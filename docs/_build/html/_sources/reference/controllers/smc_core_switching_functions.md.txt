# controllers.smc.core.switching_functions

**Source:** `src\controllers\smc\core\switching_functions.py`

## Module Overview

Switching Functions for SMC Chattering Reduction.

Provides continuous approximations to the discontinuous sign function used in SMC.
These functions reduce chattering while maintaining the robustness properties of SMC.

Mathematical Background:
- Sign function: sign(s) = {+1 if s>0, -1 if s<0, 0 if s=0}
- Continuous approximations smooth the switching to reduce high-frequency oscillations
- Trade-off: smoother switching reduces chattering but may increase steady-state error

## Complete Source Code

```{literalinclude} ../../../src/controllers/smc/core/switching_functions.py
:language: python
:linenos:
```

---

## Classes

### `SwitchingMethod`

**Inherits from:** `Enum`

Available switching function methods.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/core/switching_functions.py
:language: python
:pyobject: SwitchingMethod
:linenos:
```

---

### `SwitchingFunction`

Continuous switching functions for SMC chattering reduction.

Provides various approximations to the sign function, each with different
smoothness and robustness characteristics.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/core/switching_functions.py
:language: python
:pyobject: SwitchingFunction
:linenos:
```

#### Methods (8)

##### `__init__(self, method)`

Initialize switching function.

[View full source →](#method-switchingfunction-__init__)

##### `_get_switching_function(self)`

Get the appropriate switching function implementation.

[View full source →](#method-switchingfunction-_get_switching_function)

##### `compute(self, surface_value, boundary_layer)`

Compute switching function value.

[View full source →](#method-switchingfunction-compute)

##### `_tanh_switching(self, s, epsilon, slope)`

Hyperbolic tangent switching function with configurable slope.

[View full source →](#method-switchingfunction-_tanh_switching)

##### `_linear_switching(self, s, epsilon)`

Piecewise-linear saturation switching function.

[View full source →](#method-switchingfunction-_linear_switching)

##### `_sign_switching(self, s, epsilon)`

Pure sign function (discontinuous).

[View full source →](#method-switchingfunction-_sign_switching)

##### `_sigmoid_switching(self, s, epsilon, slope)`

Sigmoid switching function with configurable slope.

[View full source →](#method-switchingfunction-_sigmoid_switching)

##### `get_derivative(self, surface_value, boundary_layer)`

Compute derivative of switching function.

[View full source →](#method-switchingfunction-get_derivative)

---

## Functions

### `tanh_switching(s, epsilon, slope)`

Hyperbolic tangent switching function with optimized slope.

Args:
    s: Sliding surface value
    epsilon: Boundary layer thickness
    slope: Slope parameter (default: 3.0 for optimal chattering reduction)

Returns:
    tanh((slope * s)/ε) ∈ [-1, 1]

Note:
    Default slope reduced from steep (10+) to gentle (3.0) for better
    chattering reduction. Use slope=2-5 for smooth control, slope>5
    approaches discontinuous behavior.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/core/switching_functions.py
:language: python
:pyobject: tanh_switching
:linenos:
```

---

### `linear_switching(s, epsilon)`

Linear saturation switching function.

Args:
    s: Sliding surface value
    epsilon: Boundary layer thickness

Returns:
    sat(s/ε) = clip(s/ε, -1, 1)

#### Source Code

```{literalinclude} ../../../src/controllers/smc/core/switching_functions.py
:language: python
:pyobject: linear_switching
:linenos:
```

---

### `sign_switching(s, epsilon)`

Pure sign function (DEPRECATED - causes severe chattering).

WARNING: Discontinuous switching causes chattering in real systems.
Prefer tanh_switching() or linear_switching() with appropriate boundary layer.

Args:
    s: Sliding surface value
    epsilon: Ignored (kept for interface consistency)

Returns:
    sign(s) ∈ {-1, 0, 1}

Deprecated:
    Use tanh_switching(s, epsilon, slope=3.0) instead for chattering reduction.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/core/switching_functions.py
:language: python
:pyobject: sign_switching
:linenos:
```

---

### `adaptive_boundary_layer(surface_value, surface_derivative, base_epsilon, adaptation_gain)`

Adaptive boundary layer thickness based on surface derivative.

Larger ε when |ṡ| is large (fast surface motion) to increase smoothness.
Smaller ε when |ṡ| is small (near surface) to maintain precision.

Args:
    surface_value: Current sliding surface value
    surface_derivative: Surface time derivative ṡ
    base_epsilon: Base boundary layer thickness
    adaptation_gain: Adaptation coefficient

Returns:
    Adaptive boundary layer thickness

#### Source Code

```{literalinclude} ../../../src/controllers/smc/core/switching_functions.py
:language: python
:pyobject: adaptive_boundary_layer
:linenos:
```

---

### `power_rate_reaching_law(surface_value, K, alpha, epsilon)`

Power rate reaching law for finite-time convergence.

Formula: -K * |s|^α * sign(s) ≈ -K * |s|^α * tanh(s/ε)

Args:
    surface_value: Sliding surface value s
    K: Reaching law gain (> 0)
    alpha: Power exponent (0 < α < 1 for finite-time)
    epsilon: Boundary layer for sign approximation

Returns:
    Power rate reaching law output

#### Source Code

```{literalinclude} ../../../src/controllers/smc/core/switching_functions.py
:language: python
:pyobject: power_rate_reaching_law
:linenos:
```

---

## Dependencies

This module imports:

- `from typing import Union, Callable`
- `import numpy as np`
- `from enum import Enum`
