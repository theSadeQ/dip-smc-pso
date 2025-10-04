# interfaces.hil.fault_injection

**Source:** `src\interfaces\hil\fault_injection.py`

## Module Overview

Fault injection system for HIL testing and validation.
This module provides comprehensive fault injection capabilities including
sensor faults, actuator faults, communication failures, and system-level
fault scenarios for robust control system testing.

## Complete Source Code

```{literalinclude} ../../../src/interfaces/hil/fault_injection.py
:language: python
:linenos:
```

---

## Classes

### `FaultType`

**Inherits from:** `Enum`

Fault type enumeration.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/fault_injection.py
:language: python
:pyobject: FaultType
:linenos:
```

---

### `FaultSeverity`

**Inherits from:** `Enum`

Fault severity enumeration.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/fault_injection.py
:language: python
:pyobject: FaultSeverity
:linenos:
```

---

### `FaultProfile`

Fault injection profile configuration.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/fault_injection.py
:language: python
:pyobject: FaultProfile
:linenos:
```

---

### `FaultScenario`

Complete fault scenario with multiple fault profiles.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/fault_injection.py
:language: python
:pyobject: FaultScenario
:linenos:
```

---

### `FaultEvent`

Fault event record.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/fault_injection.py
:language: python
:pyobject: FaultEvent
:linenos:
```

---

### `FaultInjector`

Comprehensive fault injection system for HIL testing.

Provides systematic fault injection capabilities for sensors,
actuators, communication, and system-level components to validate
control system robustness and fault tolerance.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/fault_injection.py
:language: python
:pyobject: FaultInjector
:linenos:
```

#### Methods (29)

##### `__init__(self, device_manager, communication_interfaces)`

Initialize fault injector.

[View full source →](#method-faultinjector-__init__)

##### `enabled(self)`

Check if fault injection is enabled.

[View full source →](#method-faultinjector-enabled)

##### `active_faults(self)`

Get currently active faults.

[View full source →](#method-faultinjector-active_faults)

##### `statistics(self)`

Get fault injection statistics.

[View full source →](#method-faultinjector-statistics)

##### `enable(self)`

Enable fault injection.

[View full source →](#method-faultinjector-enable)

##### `disable(self)`

Disable fault injection.

[View full source →](#method-faultinjector-disable)

##### `inject_fault(self, fault_id, profile)`

Inject a specific fault.

[View full source →](#method-faultinjector-inject_fault)

##### `remove_fault(self, fault_id)`

Remove an active fault.

[View full source →](#method-faultinjector-remove_fault)

##### `clear_all_faults(self)`

Clear all active faults.

[View full source →](#method-faultinjector-clear_all_faults)

##### `configure_scenario(self, scenario)`

Configure fault scenario.

[View full source →](#method-faultinjector-configure_scenario)

##### `execute_scenario(self, scenario_name)`

Execute fault scenario.

[View full source →](#method-faultinjector-execute_scenario)

##### `stop_scenario(self)`

Stop current scenario execution.

[View full source →](#method-faultinjector-stop_scenario)

##### `get_fault_history(self, since, fault_type)`

Get fault event history.

[View full source →](#method-faultinjector-get_fault_history)

##### `_execute_fault(self, fault_id, profile)`

Execute fault injection task.

[View full source →](#method-faultinjector-_execute_fault)

##### `_apply_fault(self, device, profile)`

Apply specific fault to device.

[View full source →](#method-faultinjector-_apply_fault)

##### `_apply_sensor_bias(self, device, profile)`

Apply sensor bias fault.

[View full source →](#method-faultinjector-_apply_sensor_bias)

##### `_apply_sensor_drift(self, device, profile)`

Apply sensor drift fault.

[View full source →](#method-faultinjector-_apply_sensor_drift)

##### `_apply_sensor_noise(self, device, profile)`

Apply sensor noise fault.

[View full source →](#method-faultinjector-_apply_sensor_noise)

##### `_apply_sensor_stuck(self, device, profile)`

Apply sensor stuck fault.

[View full source →](#method-faultinjector-_apply_sensor_stuck)

##### `_apply_actuator_bias(self, device, profile)`

Apply actuator bias fault.

[View full source →](#method-faultinjector-_apply_actuator_bias)

##### `_apply_actuator_stuck(self, device, profile)`

Apply actuator stuck fault.

[View full source →](#method-faultinjector-_apply_actuator_stuck)

##### `_apply_communication_delay(self, profile)`

Apply communication delay fault.

[View full source →](#method-faultinjector-_apply_communication_delay)

##### `_apply_communication_loss(self, profile)`

Apply communication loss fault.

[View full source →](#method-faultinjector-_apply_communication_loss)

##### `_execute_scenario_task(self, scenario)`

Execute complete fault scenario.

[View full source →](#method-faultinjector-_execute_scenario_task)

##### `_inject_scenario_fault(self, fault_id, profile)`

Inject fault as part of scenario.

[View full source →](#method-faultinjector-_inject_scenario_fault)

##### `_validate_fault_profile(self, profile)`

Validate fault profile configuration.

[View full source →](#method-faultinjector-_validate_fault_profile)

##### `_cleanup_fault(self, fault_id, profile)`

Clean up fault after completion or cancellation.

[View full source →](#method-faultinjector-_cleanup_fault)

##### `_record_fault_event(self, event)`

Record fault event in history.

[View full source →](#method-faultinjector-_record_fault_event)

##### `set_safety_limits(self, device_id, limits)`

Set safety limits for fault injection.

[View full source →](#method-faultinjector-set_safety_limits)

---

## Functions

### `create_sensor_fault_scenario(sensor_name, fault_types, duration)`

Create common sensor fault scenario.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/fault_injection.py
:language: python
:pyobject: create_sensor_fault_scenario
:linenos:
```

---

### `create_actuator_fault_scenario(actuator_name, severity)`

Create common actuator fault scenario.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/fault_injection.py
:language: python
:pyobject: create_actuator_fault_scenario
:linenos:
```

---

## Dependencies

This module imports:

- `import asyncio`
- `import time`
- `import random`
- `import numpy as np`
- `from dataclasses import dataclass, field`
- `from typing import Dict, Any, Optional, List, Callable, Union`
- `from enum import Enum`
- `import logging`
