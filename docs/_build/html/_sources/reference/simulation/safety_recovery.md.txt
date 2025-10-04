# simulation.safety.recovery

**Source:** `src\simulation\safety\recovery.py`

## Module Overview

Safety recovery strategies for simulation framework.

## Complete Source Code

```{literalinclude} ../../../src/simulation/safety/recovery.py
:language: python
:linenos:
```

---

## Classes

### `RecoveryStrategy`

**Inherits from:** `ABC`

Base class for safety recovery strategies.

#### Source Code

```{literalinclude} ../../../src/simulation/safety/recovery.py
:language: python
:pyobject: RecoveryStrategy
:linenos:
```

#### Methods (1)

##### `recover(self, state, control, violation_info)`

Implement recovery strategy.

[View full source →](#method-recoverystrategy-recover)

---

### `EmergencyStop`

**Inherits from:** `RecoveryStrategy`

Emergency stop recovery strategy.

#### Source Code

```{literalinclude} ../../../src/simulation/safety/recovery.py
:language: python
:pyobject: EmergencyStop
:linenos:
```

#### Methods (1)

##### `recover(self, state, control, violation_info)`

Apply emergency stop - zero control and hold state.

[View full source →](#method-emergencystop-recover)

---

### `StateLimiter`

**Inherits from:** `RecoveryStrategy`

State limiting recovery strategy.

#### Source Code

```{literalinclude} ../../../src/simulation/safety/recovery.py
:language: python
:pyobject: StateLimiter
:linenos:
```

#### Methods (2)

##### `__init__(self, lower_bounds, upper_bounds)`

Initialize state limiter.

[View full source →](#method-statelimiter-__init__)

##### `recover(self, state, control, violation_info)`

Clip state to bounds and reduce control.

[View full source →](#method-statelimiter-recover)

---

### `SafetyRecovery`

Safety recovery manager.

#### Source Code

```{literalinclude} ../../../src/simulation/safety/recovery.py
:language: python
:pyobject: SafetyRecovery
:linenos:
```

#### Methods (3)

##### `__init__(self)`

Initialize safety recovery manager.

[View full source →](#method-safetyrecovery-__init__)

##### `register_strategy(self, violation_type, strategy)`

Register recovery strategy for specific violation type.

[View full source →](#method-safetyrecovery-register_strategy)

##### `apply_recovery(self, state, control, violation_info)`

Apply appropriate recovery strategy.

[View full source →](#method-safetyrecovery-apply_recovery)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from abc import ABC, abstractmethod`
- `from typing import Any, Optional`
- `import numpy as np`
