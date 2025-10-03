# interfaces.hil.plant_server

**Source:** `src\interfaces\hil\plant_server.py`

## Module Overview

*No module docstring available.*

## Complete Source Code

```{literalinclude} ../../../src/interfaces/hil/plant_server.py
:language: python
:linenos:
```

---

## Classes

### `PlantServer`

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/plant_server.py
:language: python
:pyobject: PlantServer
:linenos:
```

#### Methods (4)

##### `__init__(self, cfg, bind_addr, dt, extra_latency_ms, sensor_noise_std, max_steps, server_ready_event)`

[View full source →](#method-plantserver-__init__)

##### `start(self)`

[View full source →](#method-plantserver-start)

##### `close(self)`

[View full source →](#method-plantserver-close)

##### `stop(self)`

[View full source →](#method-plantserver-stop)

---

## Functions

### `_load_config(cfg_path)`

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/plant_server.py
:language: python
:pyobject: _load_config
:linenos:
```

---

### `_get(cfg, dotted, default)`

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/plant_server.py
:language: python
:pyobject: _get
:linenos:
```

---

### `_build_dynamics(cfg)`

Build the dynamics model using the project's light/full models if present.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/plant_server.py
:language: python
:pyobject: _build_dynamics
:linenos:
```

---

### `start_server(cfg_path, max_steps)`

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/plant_server.py
:language: python
:pyobject: start_server
:linenos:
```

---

### `main(argv)`

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/plant_server.py
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
- `import threading`
- `import time`
- `import logging`
- `from pathlib import Path`
- `from typing import Optional, Tuple`

*... and 1 more*
