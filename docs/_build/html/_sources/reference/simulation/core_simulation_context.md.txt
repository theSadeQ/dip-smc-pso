# simulation.core.simulation_context

**Source:** `src\simulation\core\simulation_context.py`

## Module Overview

Enhanced simulation context management with framework integration.

## Complete Source Code

```{literalinclude} ../../../src/simulation/core/simulation_context.py
:language: python
:linenos:
```

---

## Classes

### `SimulationContext`

Enhanced simulation context with framework integration.

Centralizes simulation setup including configuration loading,
dynamics model selection, and framework component initialization.

#### Source Code

```{literalinclude} ../../../src/simulation/core/simulation_context.py
:language: python
:pyobject: SimulationContext
:linenos:
```

#### Methods (10)

##### `__init__(self, config_path)`

Initialize the simulation context.

[View full source →](#method-simulationcontext-__init__)

##### `_initialize_dynamics_model(self)`

Initialize the dynamics model based on configuration.

[View full source →](#method-simulationcontext-_initialize_dynamics_model)

##### `get_dynamics_model(self)`

Return the initialized dynamics model.

[View full source →](#method-simulationcontext-get_dynamics_model)

##### `get_config(self)`

Return the validated configuration.

[View full source →](#method-simulationcontext-get_config)

##### `create_controller(self, name, gains)`

Create a controller using the configuration.

[View full source →](#method-simulationcontext-create_controller)

##### `create_fdi(self)`

Create FDI system if enabled in configuration.

[View full source →](#method-simulationcontext-create_fdi)

##### `register_component(self, name, component)`

Register a simulation framework component.

[View full source →](#method-simulationcontext-register_component)

##### `get_component(self, name)`

Get a registered component.

[View full source →](#method-simulationcontext-get_component)

##### `create_simulation_engine(self, engine_type)`

Create a simulation engine of specified type.

[View full source →](#method-simulationcontext-create_simulation_engine)

##### `get_simulation_parameters(self)`

Get simulation parameters from configuration.

[View full source →](#method-simulationcontext-get_simulation_parameters)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import logging`
- `from typing import Optional, List, Any, Dict, Union`
- `from src.config import load_config, ConfigSchema`
- `from .interfaces import SimulationEngine`
- `from src.utils.config_compatibility import wrap_physics_config`
