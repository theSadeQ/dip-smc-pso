# controllers.smc.algorithms.hybrid.controller

**Source:** `src\controllers\smc\algorithms\hybrid\controller.py`

## Module Overview

Modular Hybrid SMC Controller.

Implements Hybrid Sliding Mode Control that intelligently switches between
multiple SMC algorithms based on system conditions and performance metrics.

Orchestrates:
- Multiple SMC controllers (Classical, Adaptive, Super-Twisting)
- Intelligent switching logic
- Smooth control transitions
- Performance monitoring and learning

## Complete Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/hybrid/controller.py
:language: python
:linenos:
```

---

## Classes

### `TransitionFilter`

Smoothing filter for control transitions between controllers.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/hybrid/controller.py
:language: python
:pyobject: TransitionFilter
:linenos:
```

#### Methods (3)

##### `__init__(self, time_constant)`

Initialize transition filter.

[View full source →](#method-transitionfilter-__init__)

##### `filter(self, new_input, dt)`

Apply exponential smoothing filter.

[View full source →](#method-transitionfilter-filter)

##### `reset(self, initial_value)`

Reset filter state.

[View full source →](#method-transitionfilter-reset)

---

### `ModularHybridSMC`

Modular Hybrid SMC using intelligent switching between multiple controllers.

Provides optimal performance by selecting the most appropriate SMC algorithm
based on current system conditions and performance metrics.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/hybrid/controller.py
:language: python
:pyobject: ModularHybridSMC
:linenos:
```

#### Methods (20)

##### `__init__(self, config, dynamics)`

Initialize modular hybrid SMC.

[View full source →](#method-modularhybridsmc-__init__)

##### `_initialize_controllers(self)`

Initialize individual SMC controllers based on hybrid mode.

[View full source →](#method-modularhybridsmc-_initialize_controllers)

##### `current_mode(self)`

Get current hybrid mode for test compatibility.

[View full source →](#method-modularhybridsmc-current_mode)

##### `current_mode(self, mode)`

Set current hybrid mode for test compatibility.

[View full source →](#method-modularhybridsmc-current_mode)

##### `compute_control(self, state, state_vars, history, dt)`

Compute hybrid SMC control law.

[View full source →](#method-modularhybridsmc-compute_control)

##### `_create_hybrid_result(self, u_final, active_controller, active_result, all_results, switching_decision, switched, state)`

Create comprehensive hybrid control result.

[View full source →](#method-modularhybridsmc-_create_hybrid_result)

##### `_extract_controller_specific_info(self, controller_name, result)`

Extract controller-specific information for logging.

[View full source →](#method-modularhybridsmc-_extract_controller_specific_info)

##### `_compute_tracking_error(self, state)`

Compute tracking error from system state.

[View full source →](#method-modularhybridsmc-_compute_tracking_error)

##### `_create_error_result(self, error_msg)`

Create error result with safe defaults.

[View full source →](#method-modularhybridsmc-_create_error_result)

##### `gains(self)`

Return hybrid controller surface gains [k1, k2, λ1, λ2].

[View full source →](#method-modularhybridsmc-gains)

##### `validate_gains(self, gains_b)`

Vectorized feasibility check for hybrid SMC gains.

[View full source →](#method-modularhybridsmc-validate_gains)

##### `get_active_controller_name(self)`

Get name of currently active controller.

[View full source →](#method-modularhybridsmc-get_active_controller_name)

##### `get_active_controller(self)`

Get currently active controller object.

[View full source →](#method-modularhybridsmc-get_active_controller)

##### `reset(self)`

Reset controller to initial state (standard interface).

[View full source →](#method-modularhybridsmc-reset)

##### `reset_all_controllers(self)`

Reset all individual controllers to initial state.

[View full source →](#method-modularhybridsmc-reset_all_controllers)

##### `force_switch_to_controller(self, controller_name)`

Force switch to specific controller.

[View full source →](#method-modularhybridsmc-force_switch_to_controller)

##### `get_comprehensive_analysis(self)`

Get comprehensive analysis of hybrid system performance.

[View full source →](#method-modularhybridsmc-get_comprehensive_analysis)

##### `_analyze_controller_performance(self)`

Analyze relative performance of different controllers.

[View full source →](#method-modularhybridsmc-_analyze_controller_performance)

##### `tune_switching_parameters(self)`

Tune switching parameters during runtime.

[View full source →](#method-modularhybridsmc-tune_switching_parameters)

##### `get_parameters(self)`

Get all hybrid system parameters.

[View full source →](#method-modularhybridsmc-get_parameters)

---

### `HybridSMC`

Backward-compatible facade for the modular Hybrid SMC.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/hybrid/controller.py
:language: python
:pyobject: HybridSMC
:linenos:
```

#### Methods (6)

##### `__init__(self, hybrid_mode, controller_configs, dt, max_force)`

Initialize Hybrid SMC with legacy interface.

[View full source →](#method-hybridsmc-__init__)

##### `compute_control(self, state, state_vars, history)`

Compute control (delegates to modular controller).

[View full source →](#method-hybridsmc-compute_control)

##### `gains(self)`

Return controller gains.

[View full source →](#method-hybridsmc-gains)

##### `get_active_controller_name(self)`

Get active controller name.

[View full source →](#method-hybridsmc-get_active_controller_name)

##### `reset_all_controllers(self)`

Reset all controllers.

[View full source →](#method-hybridsmc-reset_all_controllers)

##### `get_parameters(self)`

Get controller parameters.

[View full source →](#method-hybridsmc-get_parameters)

---

## Dependencies

This module imports:

- `from typing import Dict, List, Union, Optional, Any`
- `import numpy as np`
- `import logging`
- `from ..classical.controller import ModularClassicalSMC`
- `from ..adaptive.controller import ModularAdaptiveSMC`
- `from ..super_twisting.controller import ModularSuperTwistingSMC`
- `from .switching_logic import HybridSwitchingLogic, ControllerState`
- `from .config import HybridSMCConfig`
