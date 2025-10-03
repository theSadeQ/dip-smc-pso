# interfaces.hil.enhanced_hil

**Source:** `src\interfaces\hil\enhanced_hil.py`

## Module Overview

Enhanced Hardware-in-the-Loop (HIL) system for advanced control testing.
This module provides a comprehensive HIL framework with real-time capabilities,
fault injection, automated testing, and integration with hardware interfaces
for professional control system validation.

## Complete Source Code

```{literalinclude} ../../../src/interfaces/hil/enhanced_hil.py
:language: python
:linenos:
```

---

## Classes

### `HILMode`

**Inherits from:** `Enum`

HIL operation mode enumeration.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/enhanced_hil.py
:language: python
:pyobject: HILMode
:linenos:
```

---

### `HILState`

**Inherits from:** `Enum`

HIL system state enumeration.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/enhanced_hil.py
:language: python
:pyobject: HILState
:linenos:
```

---

### `TimingConfig`

HIL timing configuration.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/enhanced_hil.py
:language: python
:pyobject: TimingConfig
:linenos:
```

---

### `TestScenario`

HIL test scenario configuration.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/enhanced_hil.py
:language: python
:pyobject: TestScenario
:linenos:
```

---

### `HILConfig`

Comprehensive HIL system configuration.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/enhanced_hil.py
:language: python
:pyobject: HILConfig
:linenos:
```

---

### `EnhancedHILSystem`

Enhanced Hardware-in-the-Loop system with advanced capabilities.

This class provides a comprehensive HIL framework that integrates
simulation, hardware, real-time scheduling, fault injection,
and automated testing for professional control system validation.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/enhanced_hil.py
:language: python
:pyobject: EnhancedHILSystem
:linenos:
```

#### Methods (27)

##### `__init__(self, config)`

Initialize enhanced HIL system.

[View full source →](#method-enhancedhilsystem-__init__)

##### `state(self)`

Get current HIL system state.

[View full source →](#method-enhancedhilsystem-state)

##### `config(self)`

Get HIL configuration.

[View full source →](#method-enhancedhilsystem-config)

##### `performance_metrics(self)`

Get performance metrics.

[View full source →](#method-enhancedhilsystem-performance_metrics)

##### `initialize(self)`

Initialize HIL system components.

[View full source →](#method-enhancedhilsystem-initialize)

##### `start(self)`

Start HIL system operation.

[View full source →](#method-enhancedhilsystem-start)

##### `stop(self)`

Stop HIL system operation.

[View full source →](#method-enhancedhilsystem-stop)

##### `emergency_stop(self)`

Perform emergency stop of HIL system.

[View full source →](#method-enhancedhilsystem-emergency_stop)

##### `pause(self)`

Pause HIL system operation.

[View full source →](#method-enhancedhilsystem-pause)

##### `resume(self)`

Resume HIL system operation.

[View full source →](#method-enhancedhilsystem-resume)

##### `run_test_scenario(self, scenario)`

Run specific test scenario.

[View full source →](#method-enhancedhilsystem-run_test_scenario)

##### `get_system_status(self)`

Get comprehensive system status.

[View full source →](#method-enhancedhilsystem-get_system_status)

##### `_setup_communication(self)`

Setup communication interfaces.

[View full source →](#method-enhancedhilsystem-_setup_communication)

##### `_setup_hardware(self)`

Setup hardware devices.

[View full source →](#method-enhancedhilsystem-_setup_hardware)

##### `_setup_simulation(self)`

Setup simulation bridge.

[View full source →](#method-enhancedhilsystem-_setup_simulation)

##### `_setup_real_time(self)`

Setup real-time scheduler.

[View full source →](#method-enhancedhilsystem-_setup_real_time)

##### `_setup_fault_injection(self)`

Setup fault injection system.

[View full source →](#method-enhancedhilsystem-_setup_fault_injection)

##### `_setup_test_framework(self)`

Setup automated test framework.

[View full source →](#method-enhancedhilsystem-_setup_test_framework)

##### `_setup_data_logging(self)`

Setup data logging system.

[View full source →](#method-enhancedhilsystem-_setup_data_logging)

##### `_system_self_test(self)`

Perform comprehensive system self-test.

[View full source →](#method-enhancedhilsystem-_system_self_test)

##### `_main_loop(self)`

Main HIL execution loop.

[View full source →](#method-enhancedhilsystem-_main_loop)

##### `_read_inputs(self)`

Read inputs from all sources.

[View full source →](#method-enhancedhilsystem-_read_inputs)

##### `_update_simulation(self)`

Update simulation model.

[View full source →](#method-enhancedhilsystem-_update_simulation)

##### `_write_outputs(self)`

Write outputs to all destinations.

[View full source →](#method-enhancedhilsystem-_write_outputs)

##### `_apply_initial_conditions(self, conditions)`

Apply initial conditions for test scenario.

[View full source →](#method-enhancedhilsystem-_apply_initial_conditions)

##### `_apply_parameters(self, parameters)`

Apply parameters for test scenario.

[View full source →](#method-enhancedhilsystem-_apply_parameters)

##### `_analyze_scenario_results(self, scenario, data)`

Analyze test scenario results.

[View full source →](#method-enhancedhilsystem-_analyze_scenario_results)

---

### `TimingMonitor`

Monitor timing performance of HIL system.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/enhanced_hil.py
:language: python
:pyobject: TimingMonitor
:linenos:
```

#### Methods (3)

##### `__init__(self, timing_config)`

[View full source →](#method-timingmonitor-__init__)

##### `record_iteration(self, iteration_time)`

Record iteration timing.

[View full source →](#method-timingmonitor-record_iteration)

##### `get_statistics(self)`

Get timing statistics.

[View full source →](#method-timingmonitor-get_statistics)

---

### `HILPerformanceMetrics`

Performance metrics for HIL system.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/enhanced_hil.py
:language: python
:pyobject: HILPerformanceMetrics
:linenos:
```

#### Methods (3)

##### `__init__(self)`

[View full source →](#method-hilperformancemetrics-__init__)

##### `update(self, iteration_time)`

Update performance metrics.

[View full source →](#method-hilperformancemetrics-update)

##### `get_summary(self)`

Get performance summary.

[View full source →](#method-hilperformancemetrics-get_summary)

---

### `SafetyMonitor`

Safety monitoring for HIL system.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/enhanced_hil.py
:language: python
:pyobject: SafetyMonitor
:linenos:
```

#### Methods (3)

##### `__init__(self, config)`

[View full source →](#method-safetymonitor-__init__)

##### `check_safety(self, inputs, outputs)`

Check safety conditions.

[View full source →](#method-safetymonitor-check_safety)

##### `get_status(self)`

Get safety status.

[View full source →](#method-safetymonitor-get_status)

---

## Dependencies

This module imports:

- `import asyncio`
- `import time`
- `import numpy as np`
- `from dataclasses import dataclass, field`
- `from typing import Dict, Any, Optional, List, Callable, Union`
- `from enum import Enum`
- `import logging`
- `from ..core.protocols import CommunicationProtocol`
- `from ..hardware.device_drivers import DeviceDriver, DeviceManager`
- `from ..network.factory import NetworkInterfaceFactory`
