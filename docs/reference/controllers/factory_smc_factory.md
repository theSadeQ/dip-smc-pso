# controllers.factory.smc_factory

**Source:** `src\controllers\factory\smc_factory.py`

## Module Overview

Clean SMC Controller Factory - Focused on 4 Core SMC Controllers

Provides a unified, type-safe interface for creating SMC controllers optimized for:
- PSO parameter tuning
- Research consistency
- Performance benchmarking
- Clean separation of concerns

Design Principles:
- Single responsibility: Only SMC controllers
- Consistent interfaces: Unified parameter handling
- PSO-ready: Array-based parameter injection
- Type-safe: Explicit typing for all controllers
- Minimal: No unnecessary complexity

## Complete Source Code

```{literalinclude} ../../../src/controllers/factory/smc_factory.py
:language: python
:linenos:
```

---

## Classes

### `SMCType`

**Inherits from:** `Enum`

Enumeration of the 4 core SMC controller types.

#### Source Code

```{literalinclude} ../../../src/controllers/factory/smc_factory.py
:language: python
:pyobject: SMCType
:linenos:
```

---

### `SMCProtocol`

**Inherits from:** `Protocol`

Protocol defining the unified SMC controller interface.

#### Source Code

```{literalinclude} ../../../src/controllers/factory/smc_factory.py
:language: python
:pyobject: SMCProtocol
:linenos:
```

#### Methods (4)

##### `compute_control(self, state, state_vars, history)`

Compute control input for given state.

[View full source →](#method-smcprotocol-compute_control)

##### `initialize_state(self)`

Initialize controller internal state.

[View full source →](#method-smcprotocol-initialize_state)

##### `initialize_history(self)`

Initialize controller history tracking.

[View full source →](#method-smcprotocol-initialize_history)

##### `gains(self)`

Return controller gains.

[View full source →](#method-smcprotocol-gains)

---

### `PSOControllerWrapper`

PSO-friendly wrapper that simplifies the control interface.

#### Source Code

```{literalinclude} ../../../src/controllers/factory/smc_factory.py
:language: python
:pyobject: PSOControllerWrapper
:linenos:
```

#### Methods (3)

##### `__init__(self, controller)`

[View full source →](#method-psocontrollerwrapper-__init__)

##### `compute_control(self, state, state_vars, history)`

Flexible compute_control interface supporting both patterns:

[View full source →](#method-psocontrollerwrapper-compute_control)

##### `gains(self)`

Return controller gains.

[View full source →](#method-psocontrollerwrapper-gains)

---

### `SMCConfig`

Clean configuration for all SMC controllers.

#### Source Code

```{literalinclude} ../../../src/controllers/factory/smc_factory.py
:language: python
:pyobject: SMCConfig
:linenos:
```

#### Methods (1)

##### `__post_init__(self)`

Validate SMC configuration parameters.

[View full source →](#method-smcconfig-__post_init__)

---

### `SMCGainSpec`

Specification of gain requirements for each SMC type.

#### Source Code

```{literalinclude} ../../../src/controllers/factory/smc_factory.py
:language: python
:pyobject: SMCGainSpec
:linenos:
```

#### Methods (1)

##### `gain_bounds(self)`

Default gain bounds for PSO optimization.

[View full source →](#method-smcgainspec-gain_bounds)

---

### `SMCFactory`

Clean, focused factory for creating SMC controllers.

Optimized for:
- PSO parameter optimization
- Research benchmarking
- Type safety and consistency

#### Source Code

```{literalinclude} ../../../src/controllers/factory/smc_factory.py
:language: python
:pyobject: SMCFactory
:linenos:
```

#### Methods (8)

##### `create_controller(smc_type, config)`

Create an SMC controller with clean, validated configuration.

[View full source →](#method-smcfactory-create_controller)

##### `create_from_gains(smc_type, gains)`

PSO-friendly: Create controller directly from gains array.

[View full source →](#method-smcfactory-create_from_gains)

##### `get_gain_specification(smc_type)`

Get gain specification for an SMC controller type.

[View full source →](#method-smcfactory-get_gain_specification)

##### `list_available_controllers()`

List all available SMC controller types.

[View full source →](#method-smcfactory-list_available_controllers)

##### `_create_classical_smc(config)`

Create Classical SMC with clean parameter mapping.

[View full source →](#method-smcfactory-_create_classical_smc)

##### `_create_adaptive_smc(config)`

Create Adaptive SMC with clean parameter mapping.

[View full source →](#method-smcfactory-_create_adaptive_smc)

##### `_create_super_twisting_smc(config)`

Create Super-Twisting SMC with clean parameter mapping.

[View full source →](#method-smcfactory-_create_super_twisting_smc)

##### `_create_hybrid_smc(config)`

Create Hybrid Adaptive-STA SMC with clean parameter mapping.

[View full source →](#method-smcfactory-_create_hybrid_smc)

---

## Functions

### `create_smc_for_pso(smc_type, gains, dynamics_model_or_max_force, dt, dynamics_model)`

Convenience function optimized for PSO parameter tuning.

Supports both calling patterns:
1. create_smc_for_pso(smc_type, gains, max_force, dt, dynamics_model)
2. create_smc_for_pso(smc_type, gains, dynamics_model)

Usage:
    # In PSO fitness function
    controller = create_smc_for_pso("classical_smc", pso_params)
    performance = evaluate_controller(controller, test_scenarios)
    return performance

#### Source Code

```{literalinclude} ../../../src/controllers/factory/smc_factory.py
:language: python
:pyobject: create_smc_for_pso
:linenos:
```

---

### `get_gain_bounds_for_pso(smc_type)`

Get PSO optimization bounds for SMC controller gains.

#### Source Code

```{literalinclude} ../../../src/controllers/factory/smc_factory.py
:language: python
:pyobject: get_gain_bounds_for_pso
:linenos:
```

---

### `validate_smc_gains(smc_type, gains)`

Validate that gains are appropriate for the SMC controller type.

#### Source Code

```{literalinclude} ../../../src/controllers/factory/smc_factory.py
:language: python
:pyobject: validate_smc_gains
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from dataclasses import dataclass`
- `from enum import Enum`
- `from typing import Protocol, Union, List, Optional, Type, Dict, Any, Tuple`
- `import numpy as np`
