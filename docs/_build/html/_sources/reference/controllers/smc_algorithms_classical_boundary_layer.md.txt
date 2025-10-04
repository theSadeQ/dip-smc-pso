# controllers.smc.algorithms.classical.boundary_layer

**Source:** `src\controllers\smc\algorithms\classical\boundary_layer.py`

## Module Overview

Boundary Layer Implementation for Classical SMC.

Implements boundary layer method for chattering reduction in sliding mode control.
Extracted from the original monolithic controller to provide focused, reusable
boundary layer logic.

Mathematical Background:
- Boundary layer thickness ε controls trade-off between chattering and tracking error
- Adaptive boundary layer: ε_eff = ε + α|ṡ| adapts to surface motion
- Switching function approximates sign(s) with continuous function within ±ε

## Complete Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/classical/boundary_layer.py
:language: python
:linenos:
```

---

## Classes

### `BoundaryLayer`

Boundary layer implementation for chattering reduction.

Provides continuous approximation to discontinuous switching within
a thin layer around the sliding surface.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/classical/boundary_layer.py
:language: python
:pyobject: BoundaryLayer
:linenos:
```

#### Methods (11)

##### `__init__(self, thickness, slope, switch_method)`

Initialize boundary layer.

[View full source →](#method-boundarylayer-__init__)

##### `get_effective_thickness(self, surface_derivative)`

Compute effective boundary layer thickness.

[View full source →](#method-boundarylayer-get_effective_thickness)

##### `apply_to_surface(self, surface_value, surface_derivative)`

Apply boundary layer switching to surface value.

[View full source →](#method-boundarylayer-apply_to_surface)

##### `compute_switching_control(self, surface_value, switching_gain, surface_derivative)`

Compute switching control component.

[View full source →](#method-boundarylayer-compute_switching_control)

##### `is_in_boundary_layer(self, surface_value, surface_derivative)`

Check if system is within boundary layer.

[View full source →](#method-boundarylayer-is_in_boundary_layer)

##### `get_chattering_index(self, control_history, dt)`

Compute chattering index from control signal history using FFT-based spectral analysis.

[View full source →](#method-boundarylayer-get_chattering_index)

##### `update_thickness(self, new_thickness)`

Update base boundary layer thickness.

[View full source →](#method-boundarylayer-update_thickness)

##### `update_slope(self, new_slope)`

Update adaptive slope coefficient.

[View full source →](#method-boundarylayer-update_slope)

##### `get_parameters(self)`

Get boundary layer parameters.

[View full source →](#method-boundarylayer-get_parameters)

##### `analyze_performance(self, surface_history, control_history, dt, state_history)`

Analyze boundary layer performance with comprehensive metrics.

[View full source →](#method-boundarylayer-analyze_performance)

##### `_estimate_convergence_time(self, surface_history, dt, tolerance)`

Estimate time to converge to boundary layer.

[View full source →](#method-boundarylayer-_estimate_convergence_time)

---

## Dependencies

This module imports:

- `from typing import Union, Callable, Optional`
- `import numpy as np`
- `from ...core.switching_functions import SwitchingFunction`
