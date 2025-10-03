# controllers.smc.algorithms.hybrid.switching_logic

**Source:** `src\controllers\smc\algorithms\hybrid\switching_logic.py`

## Module Overview

Hybrid Switching Logic for Multi-Controller SMC.

Implements intelligent switching between multiple SMC controllers based on:
- System performance metrics
- Operating conditions
- Predictive analysis
- Learning algorithms

Mathematical Background:
- Switching functions prevent controller chattering
- Hysteresis bands ensure stable transitions
- Performance indices guide optimal controller selection

## Complete Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/hybrid/switching_logic.py
:language: python
:linenos:
```

---

## Classes

### `ControllerState`

**Inherits from:** `Enum`

Current active controller state.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/hybrid/switching_logic.py
:language: python
:pyobject: ControllerState
:linenos:
```

---

### `SwitchingDecision`

Represents a switching decision with reasoning.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/hybrid/switching_logic.py
:language: python
:pyobject: SwitchingDecision
:linenos:
```

#### Methods (1)

##### `__init__(self, target_controller, reason, confidence, metrics)`

[View full source →](#method-switchingdecision-__init__)

---

### `HybridSwitchingLogic`

Intelligent switching logic for hybrid SMC controllers.

Manages controller selection based on system performance,
operating conditions, and learned preferences.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/algorithms/hybrid/switching_logic.py
:language: python
:pyobject: HybridSwitchingLogic
:linenos:
```

#### Methods (16)

##### `__init__(self, config)`

Initialize hybrid switching logic.

[View full source →](#method-hybridswitchinglogic-__init__)

##### `evaluate_switching(self, system_state, control_results, current_time)`

Evaluate whether to switch controllers.

[View full source →](#method-hybridswitchinglogic-evaluate_switching)

##### `execute_switch(self, decision, current_time)`

Execute a switching decision.

[View full source →](#method-hybridswitchinglogic-execute_switch)

##### `get_current_controller(self)`

Get name of currently active controller.

[View full source →](#method-hybridswitchinglogic-get_current_controller)

##### `_update_performance_metrics(self, control_results, system_state)`

Update performance metrics for all controllers.

[View full source →](#method-hybridswitchinglogic-_update_performance_metrics)

##### `_evaluate_surface_magnitude_switching(self, control_results)`

Evaluate switching based on sliding surface magnitude.

[View full source →](#method-hybridswitchinglogic-_evaluate_surface_magnitude_switching)

##### `_evaluate_control_effort_switching(self, control_results)`

Evaluate switching based on control effort.

[View full source →](#method-hybridswitchinglogic-_evaluate_control_effort_switching)

##### `_evaluate_tracking_error_switching(self, system_state)`

Evaluate switching based on tracking error.

[View full source →](#method-hybridswitchinglogic-_evaluate_tracking_error_switching)

##### `_evaluate_adaptation_rate_switching(self, control_results)`

Evaluate switching based on adaptation rate (for adaptive controllers).

[View full source →](#method-hybridswitchinglogic-_evaluate_adaptation_rate_switching)

##### `_evaluate_performance_index_switching(self, control_results)`

Evaluate switching based on comprehensive performance index.

[View full source →](#method-hybridswitchinglogic-_evaluate_performance_index_switching)

##### `_evaluate_time_based_switching(self, current_time)`

Evaluate switching based on time (round-robin or scheduled switching).

[View full source →](#method-hybridswitchinglogic-_evaluate_time_based_switching)

##### `_check_hysteresis_condition(self, decision)`

Check if switching decision passes hysteresis condition.

[View full source →](#method-hybridswitchinglogic-_check_hysteresis_condition)

##### `_apply_predictive_analysis(self, decision, system_state)`

Apply predictive analysis to switching decision.

[View full source →](#method-hybridswitchinglogic-_apply_predictive_analysis)

##### `_update_learned_thresholds(self, decision, control_results)`

Update learned switching thresholds based on decision outcomes.

[View full source →](#method-hybridswitchinglogic-_update_learned_thresholds)

##### `get_switching_analysis(self)`

Get comprehensive analysis of switching behavior.

[View full source →](#method-hybridswitchinglogic-get_switching_analysis)

##### `_compute_switching_statistics(self)`

Compute statistics about switching behavior.

[View full source →](#method-hybridswitchinglogic-_compute_switching_statistics)

---

## Dependencies

This module imports:

- `from typing import Dict, List, Optional, Any, Tuple`
- `import numpy as np`
- `from collections import deque`
- `from enum import Enum`
- `from .config import HybridSMCConfig, SwitchingCriterion`
