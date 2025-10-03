# optimization.integration.pso_factory_bridge

**Source:** `src\optimization\integration\pso_factory_bridge.py`

## Module Overview

Advanced PSO-Factory Integration Bridge.

This module provides robust integration between PSO optimization and the controller factory
pattern, addressing fitness evaluation issues, parameter validation, and convergence diagnostics.

## Complete Source Code

```{literalinclude} ../../../src/optimization/integration/pso_factory_bridge.py
:language: python
:linenos:
```

---

## Classes

### `ControllerType`

**Inherits from:** `Enum`

Controller types for PSO optimization.

#### Source Code

```{literalinclude} ../../../src/optimization/integration/pso_factory_bridge.py
:language: python
:pyobject: ControllerType
:linenos:
```

---

### `PSOFactoryConfig`

Configuration for PSO-Factory integration.

#### Source Code

```{literalinclude} ../../../src/optimization/integration/pso_factory_bridge.py
:language: python
:pyobject: PSOFactoryConfig
:linenos:
```

---

### `EnhancedPSOFactory`

Enhanced PSO-Factory integration with advanced optimization capabilities.

#### Source Code

```{literalinclude} ../../../src/optimization/integration/pso_factory_bridge.py
:language: python
:pyobject: EnhancedPSOFactory
:linenos:
```

#### Methods (11)

##### `__init__(self, config, global_config_path)`

Initialize enhanced PSO factory.

[View full source →](#method-enhancedpsofactory-__init__)

##### `_get_controller_specifications(self)`

Get controller-specific optimization specifications.

[View full source →](#method-enhancedpsofactory-_get_controller_specifications)

##### `_get_default_gains(self, smc_type)`

Get robust default gains for controller type.

[View full source →](#method-enhancedpsofactory-_get_default_gains)

##### `create_enhanced_controller_factory(self)`

Create an enhanced controller factory with robust error handling.

[View full source →](#method-enhancedpsofactory-create_enhanced_controller_factory)

##### `create_enhanced_fitness_function(self, controller_factory)`

Create enhanced fitness function with proper simulation execution.

[View full source →](#method-enhancedpsofactory-create_enhanced_fitness_function)

##### `_evaluate_controller_performance(self, controller, gains)`

Evaluate controller performance across multiple scenarios.

[View full source →](#method-enhancedpsofactory-_evaluate_controller_performance)

##### `_simulate_scenario(self, controller, scenario)`

Simulate a specific control scenario and compute cost.

[View full source →](#method-enhancedpsofactory-_simulate_scenario)

##### `optimize_controller(self)`

Run enhanced PSO optimization with comprehensive monitoring.

[View full source →](#method-enhancedpsofactory-optimize_controller)

##### `_analyze_optimization_performance(self, pso_result)`

Analyze PSO optimization performance and convergence.

[View full source →](#method-enhancedpsofactory-_analyze_optimization_performance)

##### `_validate_optimized_controller(self, controller, gains)`

Validate the optimized controller performance.

[View full source →](#method-enhancedpsofactory-_validate_optimized_controller)

##### `get_optimization_diagnostics(self)`

Get comprehensive optimization diagnostics.

[View full source →](#method-enhancedpsofactory-get_optimization_diagnostics)

---

## Functions

### `create_optimized_controller_factory(controller_type, optimization_config)`

Create an optimized controller factory using PSO with comprehensive results.

#### Source Code

```{literalinclude} ../../../src/optimization/integration/pso_factory_bridge.py
:language: python
:pyobject: create_optimized_controller_factory
:linenos:
```

---

### `optimize_classical_smc()`

Optimize Classical SMC controller using PSO.

#### Source Code

```{literalinclude} ../../../src/optimization/integration/pso_factory_bridge.py
:language: python
:pyobject: optimize_classical_smc
:linenos:
```

---

### `optimize_adaptive_smc()`

Optimize Adaptive SMC controller using PSO.

#### Source Code

```{literalinclude} ../../../src/optimization/integration/pso_factory_bridge.py
:language: python
:pyobject: optimize_adaptive_smc
:linenos:
```

---

### `optimize_sta_smc()`

Optimize Super-Twisting SMC controller using PSO.

#### Source Code

```{literalinclude} ../../../src/optimization/integration/pso_factory_bridge.py
:language: python
:pyobject: optimize_sta_smc
:linenos:
```

---

## Dependencies

This module imports:

- `import numpy as np`
- `import logging`
- `from typing import Any, Callable, Dict, List, Optional, Tuple, Union`
- `from dataclasses import dataclass`
- `from enum import Enum`
- `from src.controllers.factory import SMCType, SMCFactory, create_smc_for_pso, get_gain_bounds_for_pso, validate_smc_gains, get_expected_gain_count`
- `from src.optimization.algorithms.pso_optimizer import PSOTuner`
- `from src.config import load_config`
- `from src.plant.configurations import ConfigurationFactory`
