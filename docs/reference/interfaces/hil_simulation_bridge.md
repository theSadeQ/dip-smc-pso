# interfaces.hil.simulation_bridge

**Source:** `src\interfaces\hil\simulation_bridge.py`

## Module Overview

Simulation bridge for HIL systems.
This module provides seamless integration between hardware components and
simulation models, enabling hybrid testing where some components are real
hardware and others are simulated models.

## Complete Source Code

```{literalinclude} ../../../src/interfaces/hil/simulation_bridge.py
:language: python
:linenos:
```

---

## Classes

### `BridgeMode`

**Inherits from:** `Enum`

Bridge operation mode.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/simulation_bridge.py
:language: python
:pyobject: BridgeMode
:linenos:
```

---

### `ModelType`

**Inherits from:** `Enum`

Simulation model type.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/simulation_bridge.py
:language: python
:pyobject: ModelType
:linenos:
```

---

### `BridgeConfig`

Configuration for simulation bridge.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/simulation_bridge.py
:language: python
:pyobject: BridgeConfig
:linenos:
```

---

### `ModelState`

State information for a simulation model.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/simulation_bridge.py
:language: python
:pyobject: ModelState
:linenos:
```

---

### `ModelInterface`

**Inherits from:** `ABC`

Abstract interface for simulation models.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/simulation_bridge.py
:language: python
:pyobject: ModelInterface
:linenos:
```

#### Methods (9)

##### `initialize(self, parameters)`

Initialize the model with given parameters.

[View full source →](#method-modelinterface-initialize)

##### `step(self, inputs, dt)`

Execute one simulation step.

[View full source →](#method-modelinterface-step)

##### `get_state(self)`

Get current model state.

[View full source →](#method-modelinterface-get_state)

##### `set_state(self, state)`

Set model state.

[View full source →](#method-modelinterface-set_state)

##### `reset(self)`

Reset model to initial state.

[View full source →](#method-modelinterface-reset)

##### `cleanup(self)`

Clean up model resources.

[View full source →](#method-modelinterface-cleanup)

##### `model_type(self)`

Get model type.

[View full source →](#method-modelinterface-model_type)

##### `input_names(self)`

Get list of input signal names.

[View full source →](#method-modelinterface-input_names)

##### `output_names(self)`

Get list of output signal names.

[View full source →](#method-modelinterface-output_names)

---

### `PlantModel`

**Inherits from:** `ModelInterface`

Base class for plant simulation models.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/simulation_bridge.py
:language: python
:pyobject: PlantModel
:linenos:
```

#### Methods (7)

##### `__init__(self, model_id)`

[View full source →](#method-plantmodel-__init__)

##### `model_type(self)`

[View full source →](#method-plantmodel-model_type)

##### `initialize(self, parameters)`

Initialize plant model.

[View full source →](#method-plantmodel-initialize)

##### `get_state(self)`

Get current plant state.

[View full source →](#method-plantmodel-get_state)

##### `set_state(self, state)`

Set plant state.

[View full source →](#method-plantmodel-set_state)

##### `reset(self)`

Reset plant to initial state.

[View full source →](#method-plantmodel-reset)

##### `cleanup(self)`

Clean up plant model.

[View full source →](#method-plantmodel-cleanup)

---

### `LinearPlantModel`

**Inherits from:** `PlantModel`

Linear plant model implementation.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/simulation_bridge.py
:language: python
:pyobject: LinearPlantModel
:linenos:
```

#### Methods (5)

##### `__init__(self, model_id)`

[View full source →](#method-linearplantmodel-__init__)

##### `input_names(self)`

[View full source →](#method-linearplantmodel-input_names)

##### `output_names(self)`

[View full source →](#method-linearplantmodel-output_names)

##### `initialize(self, parameters)`

Initialize linear plant model.

[View full source →](#method-linearplantmodel-initialize)

##### `step(self, inputs, dt)`

Execute linear plant simulation step.

[View full source →](#method-linearplantmodel-step)

---

### `SignalMapper`

Maps signals between hardware and simulation components.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/simulation_bridge.py
:language: python
:pyobject: SignalMapper
:linenos:
```

#### Methods (4)

##### `__init__(self)`

[View full source →](#method-signalmapper-__init__)

##### `add_mapping(self, source, destination, transformation, scaling, offset)`

Add signal mapping.

[View full source →](#method-signalmapper-add_mapping)

##### `map_signal(self, source, value)`

Map signal from source to destination.

[View full source →](#method-signalmapper-map_signal)

##### `get_mappings(self)`

Get all signal mappings.

[View full source →](#method-signalmapper-get_mappings)

---

### `SimulationBridge`

Main simulation bridge for HIL systems.

Coordinates execution between hardware components and simulation models,
ensuring proper timing, data flow, and synchronization.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/simulation_bridge.py
:language: python
:pyobject: SimulationBridge
:linenos:
```

#### Methods (17)

##### `__init__(self, config)`

Initialize simulation bridge.

[View full source →](#method-simulationbridge-__init__)

##### `initialize(self)`

Initialize simulation bridge.

[View full source →](#method-simulationbridge-initialize)

##### `start(self)`

Start simulation bridge execution.

[View full source →](#method-simulationbridge-start)

##### `stop(self)`

Stop simulation bridge execution.

[View full source →](#method-simulationbridge-stop)

##### `add_model(self, model_id, model)`

Add simulation model to bridge.

[View full source →](#method-simulationbridge-add_model)

##### `remove_model(self, model_id)`

Remove simulation model from bridge.

[View full source →](#method-simulationbridge-remove_model)

##### `add_signal_mapping(self, source, destination, transformation)`

Add signal mapping between components.

[View full source →](#method-simulationbridge-add_signal_mapping)

##### `set_hardware_interface(self, read_callback, write_callback)`

Set hardware interface callbacks.

[View full source →](#method-simulationbridge-set_hardware_interface)

##### `execute_step(self)`

Execute one simulation/HIL step.

[View full source →](#method-simulationbridge-execute_step)

##### `run_continuous(self, duration)`

Run simulation bridge continuously.

[View full source →](#method-simulationbridge-run_continuous)

##### `pause(self)`

Pause simulation bridge execution.

[View full source →](#method-simulationbridge-pause)

##### `resume(self)`

Resume simulation bridge execution.

[View full source →](#method-simulationbridge-resume)

##### `get_performance_statistics(self)`

Get performance statistics.

[View full source →](#method-simulationbridge-get_performance_statistics)

##### `_map_inputs_for_model(self, model, hardware_inputs, model_outputs)`

Map inputs for a specific model.

[View full source →](#method-simulationbridge-_map_inputs_for_model)

##### `_map_outputs_to_hardware(self, model_outputs)`

Map model outputs to hardware signals.

[View full source →](#method-simulationbridge-_map_outputs_to_hardware)

##### `_update_buffers(self, inputs, outputs)`

Update data buffers.

[View full source →](#method-simulationbridge-_update_buffers)

##### `_synchronize_real_time(self)`

Synchronize with real-time execution.

[View full source →](#method-simulationbridge-_synchronize_real_time)

---

## Functions

### `create_linear_plant_model(model_id, A, B, C, D)`

Create linear plant model with state-space matrices.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/simulation_bridge.py
:language: python
:pyobject: create_linear_plant_model
:linenos:
```

---

### `create_simulation_bridge(sample_time, real_time_factor)`

Create simulation bridge with default configuration.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/simulation_bridge.py
:language: python
:pyobject: create_simulation_bridge
:linenos:
```

---

## Dependencies

This module imports:

- `import asyncio`
- `import time`
- `import numpy as np`
- `from abc import ABC, abstractmethod`
- `from dataclasses import dataclass, field`
- `from typing import Dict, Any, Optional, List, Callable, Union`
- `from enum import Enum`
- `import logging`
