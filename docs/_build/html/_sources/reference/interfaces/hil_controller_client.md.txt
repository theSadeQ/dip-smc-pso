# interfaces.hil.controller_client

**Source:** `src\interfaces\hil\controller_client.py`

## Module Overview

*No module docstring available.*

## Complete Source Code

```{literalinclude} ../../../src/interfaces/hil/controller_client.py
:language: python
:linenos:
```

---

## Classes

### `_FallbackPDController`

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/controller_client.py
:language: python
:pyobject: _FallbackPDController
:linenos:
```

#### Methods (4)

##### `__init__(self)`

[View full source →](#method-_fallbackpdcontroller-__init__)

##### `initialize_state(self)`

[View full source →](#method-_fallbackpdcontroller-initialize_state)

##### `initialize_history(self)`

[View full source →](#method-_fallbackpdcontroller-initialize_history)

##### `compute_control(self, state, state_vars, history)`

[View full source →](#method-_fallbackpdcontroller-compute_control)

---

### `HILControllerClient`

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/controller_client.py
:language: python
:pyobject: HILControllerClient
:linenos:
```

#### Methods (2)

##### `__init__(self, cfg, plant_addr, bind_addr, dt, steps, results_path, loop_sleep, recv_timeout_s)`

[View full source →](#method-hilcontrollerclient-__init__)

##### `run(self)`

[View full source →](#method-hilcontrollerclient-run)

---

## Functions

### `_load_config(cfg_path)`

Prefer validated loading; fallback to YAML only if project loader unavailable.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/controller_client.py
:language: python
:pyobject: _load_config
:linenos:
```

---

### `_get(cfg, dotted, default)`

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/controller_client.py
:language: python
:pyobject: _get
:linenos:
```

---

### `_build_controller(cfg)`

Instantiate the configured controller or raise an error.

In earlier versions this function silently fell back to a built‑in
PD controller when the factory failed.  Such silent fallbacks can
obscure configuration errors (e.g., mis‑spelling a controller name)
and lead to unexpected behaviour.  We now raise a ``RuntimeError``
when the controller cannot be created.  Failing fast on
misconfiguration prevents experiments from silently using an
unintended controller.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/controller_client.py
:language: python
:pyobject: _build_controller
:linenos:
```

---

### `run_client(cfg_path, steps, results_path)`

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/controller_client.py
:language: python
:pyobject: run_client
:linenos:
```

---

### `main(argv)`

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/controller_client.py
:language: python
:pyobject: main
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import argparse`
- `import socket`
- `import struct`
- `import zlib`
- `import time`
- `from pathlib import Path`
- `from typing import Optional, Tuple`
- `import numpy as np`
