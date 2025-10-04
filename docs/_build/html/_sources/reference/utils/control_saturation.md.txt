# utils.control.saturation

**Source:** `src\utils\control\saturation.py`

## Module Overview

Saturation functions for sliding mode control.

Provides continuous approximations of the sign function to reduce chattering
in sliding mode controllers.

## Complete Source Code

```{literalinclude} ../../../src/utils/control/saturation.py
:language: python
:linenos:
```

---

## Functions

### `saturate(sigma, epsilon, method, slope)`

Continuous approximation of sign(sigma) within a boundary layer.

Args:
    sigma: Sliding surface value(s).
    epsilon: Boundary-layer half-width in σ-space (must be > 0).
    method: "tanh" (default) uses tanh((slope * sigma)/epsilon);
            "linear" uses clip(sigma/epsilon, -1, 1).
    slope: Slope parameter for tanh switching (default: 3.0).
           Lower values (2-5) provide smoother transitions and better
           chattering reduction. Original implicit steep slopes (10+)
           behaved like discontinuous sign function.
Returns:
    Same shape as `sigma`.

Notes
-----
The boundary layer width ``epsilon`` should be chosen based on the
expected amplitude of measurement noise and the desired steady‑state
accuracy. A larger ``epsilon`` reduces chattering but introduces
a finite steady‑state error; conversely, a smaller ``epsilon`` reduces
error but may increase high‑frequency switching.

The slope parameter (default 3.0) was optimized for Issue #12 chattering
reduction. Lower slope values provide smoother control signals at the cost
of slightly reduced tracking accuracy near the sliding surface.

Raises:
    ValueError
        If ``epsilon <= 0`` or an unknown ``method`` is provided.

#### Source Code

```{literalinclude} ../../../src/utils/control/saturation.py
:language: python
:pyobject: saturate
:linenos:
```

---

### `smooth_sign(x, epsilon)`

Smooth approximation of the sign function using tanh.

Args:
    x: Input value(s).
    epsilon: Smoothing parameter.

Returns:
    Smooth sign approximation.

#### Source Code

```{literalinclude} ../../../src/utils/control/saturation.py
:language: python
:pyobject: smooth_sign
:linenos:
```

---

### `dead_zone(x, threshold)`

Apply dead zone to input signal.

Args:
    x: Input signal.
    threshold: Dead zone threshold (must be positive).

Returns:
    Signal with dead zone applied.

#### Source Code

```{literalinclude} ../../../src/utils/control/saturation.py
:language: python
:pyobject: dead_zone
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import numpy as np`
- `import warnings`
- `from typing import Literal, Union`
