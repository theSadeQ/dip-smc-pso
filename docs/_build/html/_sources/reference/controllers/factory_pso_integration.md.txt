# controllers.factory.pso_integration

**Source:** `src\controllers\factory\pso_integration.py`

## Module Overview

Advanced PSO Integration Module for SMC Controllers.

This module provides optimized integration between SMC controllers and PSO optimization,
featuring thread-safe operations, performance monitoring, and comprehensive error handling.

## Complete Source Code

```{literalinclude} ../../../src/controllers/factory/pso_integration.py
:language: python
:linenos:
```

---

## Classes

### `PSOOptimizable`

**Inherits from:** `Protocol`

Protocol for PSO-optimizable controllers.

#### Source Code

```{literalinclude} ../../../src/controllers/factory/pso_integration.py
:language: python
:pyobject: PSOOptimizable
:linenos:
```

#### Methods (2)

##### `compute_control(self, state)`

Compute control output for given state.

[View full source →](#method-psooptimizable-compute_control)

##### `max_force(self)`

Maximum control force limit.

[View full source →](#method-psooptimizable-max_force)

---

### `PSOPerformanceMetrics`

Performance metrics for PSO controller evaluation.

#### Source Code

```{literalinclude} ../../../src/controllers/factory/pso_integration.py
:language: python
:pyobject: PSOPerformanceMetrics
:linenos:
```

---

### `EnhancedPSOControllerWrapper`

Enhanced PSO-compatible controller wrapper with advanced features.

Features:
- Thread-safe operation
- Performance monitoring
- Automatic saturation handling
- Error recovery mechanisms
- Statistical tracking

#### Source Code

```{literalinclude} ../../../src/controllers/factory/pso_integration.py
:language: python
:pyobject: EnhancedPSOControllerWrapper
:linenos:
```

#### Methods (10)

##### `__init__(self, controller, controller_type, max_force, enable_monitoring)`

Initialize enhanced PSO wrapper.

[View full source →](#method-enhancedpsocontrollerwrapper-__init__)

##### `compute_control(self, state)`

PSO-compatible control computation with enhanced error handling.

[View full source →](#method-enhancedpsocontrollerwrapper-compute_control)

##### `_validate_state(self, state)`

Validate input state vector.

[View full source →](#method-enhancedpsocontrollerwrapper-_validate_state)

##### `_extract_control_value(self, result)`

Extract control value from controller result.

[View full source →](#method-enhancedpsocontrollerwrapper-_extract_control_value)

##### `_apply_safety_constraints(self, control_value)`

Apply safety constraints to control value.

[View full source →](#method-enhancedpsocontrollerwrapper-_apply_safety_constraints)

##### `_get_safe_fallback_control(self, state)`

Generate safe fallback control for error conditions.

[View full source →](#method-enhancedpsocontrollerwrapper-_get_safe_fallback_control)

##### `_update_metrics(self, computation_time, control_value)`

Update performance metrics.

[View full source →](#method-enhancedpsocontrollerwrapper-_update_metrics)

##### `get_performance_metrics(self)`

Get current performance metrics.

[View full source →](#method-enhancedpsocontrollerwrapper-get_performance_metrics)

##### `reset_metrics(self)`

Reset performance metrics.

[View full source →](#method-enhancedpsocontrollerwrapper-reset_metrics)

##### `n_gains(self)`

Number of gains for PSO compatibility.

[View full source →](#method-enhancedpsocontrollerwrapper-n_gains)

---

## Functions

### `create_enhanced_pso_controller(smc_type, gains, plant_config, max_force, dt, enable_monitoring)`

Create enhanced PSO-compatible controller with advanced features.

Args:
    smc_type: SMC controller type
    gains: Controller gains
    plant_config: Plant configuration (optional)
    max_force: Maximum control force
    dt: Control timestep
    enable_monitoring: Enable performance monitoring
    **kwargs: Additional controller parameters

Returns:
    Enhanced PSO controller wrapper

Raises:
    ValueError: If parameters are invalid

#### Source Code

```{literalinclude} ../../../src/controllers/factory/pso_integration.py
:language: python
:pyobject: create_enhanced_pso_controller
:linenos:
```

---

### `create_optimized_pso_factory(smc_type, plant_config, max_force, enable_monitoring)`

Create optimized PSO factory function for controller creation.

Args:
    smc_type: SMC controller type
    plant_config: Plant configuration (optional)
    max_force: Maximum control force
    enable_monitoring: Enable performance monitoring
    **kwargs: Additional factory parameters

Returns:
    Factory function that creates PSO controllers from gains

#### Source Code

```{literalinclude} ../../../src/controllers/factory/pso_integration.py
:language: python
:pyobject: create_optimized_pso_factory
:linenos:
```

---

### `get_optimized_pso_bounds(smc_type, performance_target)`

Get optimized PSO bounds based on performance targets.

Args:
    smc_type: Controller type
    performance_target: 'aggressive', 'balanced', or 'conservative'

Returns:
    Tuple of (lower_bounds, upper_bounds)

#### Source Code

```{literalinclude} ../../../src/controllers/factory/pso_integration.py
:language: python
:pyobject: get_optimized_pso_bounds
:linenos:
```

---

### `validate_pso_gains_advanced(smc_type, gains, check_stability)`

Advanced validation of PSO gains with stability analysis.

Args:
    smc_type: Controller type
    gains: Gains to validate
    check_stability: Perform stability checks

Returns:
    Dictionary with validation results

#### Source Code

```{literalinclude} ../../../src/controllers/factory/pso_integration.py
:language: python
:pyobject: validate_pso_gains_advanced
:linenos:
```

---

## Dependencies

This module imports:

- `import logging`
- `import time`
- `from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple, Union`
- `from dataclasses import dataclass`
- `from abc import ABC, abstractmethod`
- `import numpy as np`
- `from ..factory import SMCType, create_controller, CONTROLLER_REGISTRY`
