# analysis.fault_detection.residual_generators

**Source:** `src\analysis\fault_detection\residual_generators.py`

## Module Overview

Model-based residual generation for fault detection.

This module provides various residual generation methods for fault detection
including observer-based, parity-based, and parameter estimation approaches.

## Complete Source Code

```{literalinclude} ../../../src/analysis/fault_detection/residual_generators.py
:language: python
:linenos:
```

---

## Classes

### `SystemModel`

**Inherits from:** `Protocol`

Protocol for system models used in residual generation.

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/residual_generators.py
:language: python
:pyobject: SystemModel
:linenos:
```

#### Methods (2)

##### `predict(self, state, control, dt)`

Predict next state given current state and control.

[View full source →](#method-systemmodel-predict)

##### `observe(self, state)`

Compute output from state.

[View full source →](#method-systemmodel-observe)

---

### `ResidualGeneratorConfig`

Configuration for residual generators.

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/residual_generators.py
:language: python
:pyobject: ResidualGeneratorConfig
:linenos:
```

---

### `ResidualGenerator`

**Inherits from:** `ABC`

Abstract base class for residual generators.

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/residual_generators.py
:language: python
:pyobject: ResidualGenerator
:linenos:
```

#### Methods (2)

##### `generate_residual(self, data, system_model)`

Generate residual from data and system model.

[View full source →](#method-residualgenerator-generate_residual)

##### `reset(self)`

Reset generator state.

[View full source →](#method-residualgenerator-reset)

---

### `ObserverBasedGenerator`

**Inherits from:** `ResidualGenerator`

Observer-based residual generator using Luenberger observers.

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/residual_generators.py
:language: python
:pyobject: ObserverBasedGenerator
:linenos:
```

#### Methods (4)

##### `__init__(self, config, A, C)`

Initialize observer-based generator.

[View full source →](#method-observerbasedgenerator-__init__)

##### `_design_observer(self)`

Design observer gain matrix.

[View full source →](#method-observerbasedgenerator-_design_observer)

##### `generate_residual(self, data, system_model)`

Generate observer-based residual.

[View full source →](#method-observerbasedgenerator-generate_residual)

##### `reset(self)`

Reset observer state.

[View full source →](#method-observerbasedgenerator-reset)

---

### `KalmanFilterGenerator`

**Inherits from:** `ResidualGenerator`

Kalman filter-based residual generator.

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/residual_generators.py
:language: python
:pyobject: KalmanFilterGenerator
:linenos:
```

#### Methods (3)

##### `__init__(self, config, A, B, C, D)`

Initialize Kalman filter generator.

[View full source →](#method-kalmanfiltergenerator-__init__)

##### `generate_residual(self, data, system_model)`

Generate Kalman filter innovation residual.

[View full source →](#method-kalmanfiltergenerator-generate_residual)

##### `reset(self)`

Reset Kalman filter state.

[View full source →](#method-kalmanfiltergenerator-reset)

---

### `ParitySpaceGenerator`

**Inherits from:** `ResidualGenerator`

Parity space-based residual generator.

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/residual_generators.py
:language: python
:pyobject: ParitySpaceGenerator
:linenos:
```

#### Methods (4)

##### `__init__(self, config, A, B, C)`

Initialize parity space generator.

[View full source →](#method-parityspacegenerator-__init__)

##### `_compute_parity_matrices(self)`

Compute parity space matrices.

[View full source →](#method-parityspacegenerator-_compute_parity_matrices)

##### `generate_residual(self, data, system_model)`

Generate parity space residual.

[View full source →](#method-parityspacegenerator-generate_residual)

##### `reset(self)`

Reset parity space generator state.

[View full source →](#method-parityspacegenerator-reset)

---

### `ParameterEstimationGenerator`

**Inherits from:** `ResidualGenerator`

Parameter estimation-based residual generator.

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/residual_generators.py
:language: python
:pyobject: ParameterEstimationGenerator
:linenos:
```

#### Methods (4)

##### `__init__(self, config, nominal_parameters)`

Initialize parameter estimation generator.

[View full source →](#method-parameterestimationgenerator-__init__)

##### `generate_residual(self, data, system_model)`

Generate parameter estimation residual.

[View full source →](#method-parameterestimationgenerator-generate_residual)

##### `_estimate_parameters(self, states, controls, times)`

Estimate parameters from data window.

[View full source →](#method-parameterestimationgenerator-_estimate_parameters)

##### `reset(self)`

Reset parameter estimation state.

[View full source →](#method-parameterestimationgenerator-reset)

---

### `AdaptiveResidualGenerator`

**Inherits from:** `ResidualGenerator`

Adaptive residual generator that combines multiple methods.

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/residual_generators.py
:language: python
:pyobject: AdaptiveResidualGenerator
:linenos:
```

#### Methods (4)

##### `__init__(self, generators, weights)`

Initialize adaptive generator.

[View full source →](#method-adaptiveresidualgenerator-__init__)

##### `generate_residual(self, data, system_model)`

Generate adaptive residual by combining multiple methods.

[View full source →](#method-adaptiveresidualgenerator-generate_residual)

##### `_combine_residuals(self, residuals)`

Combine residuals from multiple generators.

[View full source →](#method-adaptiveresidualgenerator-_combine_residuals)

##### `reset(self)`

Reset all generators.

[View full source →](#method-adaptiveresidualgenerator-reset)

---

### `ResidualGeneratorFactory`

Factory class for creating residual generators.

This class provides a unified interface for creating different types of
residual generators used in fault detection systems.

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/residual_generators.py
:language: python
:pyobject: ResidualGeneratorFactory
:linenos:
```

#### Methods (4)

##### `create_generator(method, config)`

Create a residual generator of the specified type.

[View full source →](#method-residualgeneratorfactory-create_generator)

##### `get_available_methods()`

Get list of available residual generation methods.

[View full source →](#method-residualgeneratorfactory-get_available_methods)

##### `create_default_observer(cls, A, C)`

Create observer-based generator with default configuration.

[View full source →](#method-residualgeneratorfactory-create_default_observer)

##### `create_default_kalman(cls, A, B, C, D)`

Create Kalman filter generator with default configuration.

[View full source →](#method-residualgeneratorfactory-create_default_kalman)

---

## Functions

### `create_residual_generator(method, config)`

Factory function to create residual generators.

Parameters
----------
method : str
    Type of generator ('observer', 'kalman', 'parity', 'parameter_estimation', 'adaptive')
config : ResidualGeneratorConfig, optional
    Configuration parameters
**kwargs
    Additional parameters specific to each method

Returns
-------
ResidualGenerator
    Configured residual generator

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/residual_generators.py
:language: python
:pyobject: create_residual_generator
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Dict, List, Optional, Tuple, Any, Protocol, Callable`
- `import numpy as np`
- `from scipy import linalg, signal`
- `import warnings`
- `from dataclasses import dataclass, field`
- `from abc import ABC, abstractmethod`
- `from ..core.interfaces import DataProtocol`
