# simulation.context.simulation_context

**Source:** `src\simulation\context\simulation_context.py`

## Module Overview

Manages the simulation setup, including configuration loading and
dynamic selection of the physics model.

## Complete Source Code

```{literalinclude} ../../../src/simulation/context/simulation_context.py
:language: python
:linenos:
```

---

## Classes

### `SimulationContext`

Initializes and holds the context for a simulation run.

This class centralizes the setup logic by loading the configuration
and selecting the appropriate dynamics model based on that config.

#### Source Code

```{literalinclude} ../../../src/simulation/context/simulation_context.py
:language: python
:pyobject: SimulationContext
:linenos:
```

#### Methods (6)

##### `__init__(self, config_path)`

Initialize the simulation context by loading the configuration.

[View full source →](#method-simulationcontext-__init__)

##### `_initialize_dynamics_model(self)`

Initialize the correct dynamics model based on the configuration.

[View full source →](#method-simulationcontext-_initialize_dynamics_model)

##### `get_dynamics_model(self)`

Return the initialized dynamics model.

[View full source →](#method-simulationcontext-get_dynamics_model)

##### `get_config(self)`

Return the validated configuration model for reuse by callers.

[View full source →](#method-simulationcontext-get_config)

##### `create_controller(self, name, gains)`

Create a controller using the shared, validated config and the project factory.

[View full source →](#method-simulationcontext-create_controller)

##### `create_fdi(self)`

Create the FDI system if enabled in config; otherwise return None.

[View full source →](#method-simulationcontext-create_fdi)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import logging`
- `from typing import Optional, List, Any`
- `from src.config import load_config, ConfigSchema`
