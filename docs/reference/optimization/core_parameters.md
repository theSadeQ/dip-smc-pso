# optimization.core.parameters

**Source:** `src\optimization\core\parameters.py`

## Module Overview

Parameter space definitions and management.

## Complete Source Code

```{literalinclude} ../../../src/optimization/core/parameters.py
:language: python
:linenos:
```

---

## Classes

### `Parameter`

**Inherits from:** `ABC`

Abstract base class for optimization parameters.

#### Source Code

```{literalinclude} ../../../src/optimization/core/parameters.py
:language: python
:pyobject: Parameter
:linenos:
```

#### Methods (5)

##### `__init__(self, name, description)`

Initialize parameter.

[View full source →](#method-parameter-__init__)

##### `sample(self, n_samples, rng)`

Sample values from parameter domain.

[View full source →](#method-parameter-sample)

##### `validate(self, value)`

Validate parameter value(s).

[View full source →](#method-parameter-validate)

##### `clip(self, value)`

Clip value(s) to valid range.

[View full source →](#method-parameter-clip)

##### `bounds(self)`

Parameter bounds (lower, upper).

[View full source →](#method-parameter-bounds)

---

### `ContinuousParameter`

**Inherits from:** `Parameter`

Continuous real-valued parameter.

#### Source Code

```{literalinclude} ../../../src/optimization/core/parameters.py
:language: python
:pyobject: ContinuousParameter
:linenos:
```

#### Methods (5)

##### `__init__(self, name, lower, upper, description, log_scale)`

Initialize continuous parameter.

[View full source →](#method-continuousparameter-__init__)

##### `sample(self, n_samples, rng)`

Sample from uniform distribution.

[View full source →](#method-continuousparameter-sample)

##### `validate(self, value)`

Check if value is within bounds.

[View full source →](#method-continuousparameter-validate)

##### `clip(self, value)`

Clip to bounds.

[View full source →](#method-continuousparameter-clip)

##### `bounds(self)`

Parameter bounds.

[View full source →](#method-continuousparameter-bounds)

---

### `DiscreteParameter`

**Inherits from:** `Parameter`

Discrete parameter with finite set of values.

#### Source Code

```{literalinclude} ../../../src/optimization/core/parameters.py
:language: python
:pyobject: DiscreteParameter
:linenos:
```

#### Methods (6)

##### `__init__(self, name, values, description)`

Initialize discrete parameter.

[View full source →](#method-discreteparameter-__init__)

##### `sample(self, n_samples, rng)`

Sample from discrete values.

[View full source →](#method-discreteparameter-sample)

##### `validate(self, value)`

Check if value is in allowed set.

[View full source →](#method-discreteparameter-validate)

##### `clip(self, value)`

Find closest valid value.

[View full source →](#method-discreteparameter-clip)

##### `_find_closest(self, value)`

Find closest valid value.

[View full source →](#method-discreteparameter-_find_closest)

##### `bounds(self)`

Bounds for discrete parameter (min and max values).

[View full source →](#method-discreteparameter-bounds)

---

### `ContinuousParameterSpace`

**Inherits from:** `ParameterSpace`

Continuous parameter space with box constraints.

#### Source Code

```{literalinclude} ../../../src/optimization/core/parameters.py
:language: python
:pyobject: ContinuousParameterSpace
:linenos:
```

#### Methods (7)

##### `__init__(self, lower_bounds, upper_bounds, names)`

Initialize continuous parameter space.

[View full source →](#method-continuousparameterspace-__init__)

##### `sample(self, n_samples, rng)`

Sample uniformly from parameter space.

[View full source →](#method-continuousparameterspace-sample)

##### `validate(self, parameters)`

Check if parameters are within bounds.

[View full source →](#method-continuousparameterspace-validate)

##### `clip(self, parameters)`

Clip parameters to bounds.

[View full source →](#method-continuousparameterspace-clip)

##### `dimensions(self)`

Number of parameters.

[View full source →](#method-continuousparameterspace-dimensions)

##### `bounds(self)`

Parameter bounds.

[View full source →](#method-continuousparameterspace-bounds)

##### `get_parameter_info(self)`

Get information about each parameter.

[View full source →](#method-continuousparameterspace-get_parameter_info)

---

### `MixedParameterSpace`

**Inherits from:** `ParameterSpace`

Mixed parameter space with continuous and discrete parameters.

#### Source Code

```{literalinclude} ../../../src/optimization/core/parameters.py
:language: python
:pyobject: MixedParameterSpace
:linenos:
```

#### Methods (6)

##### `__init__(self, parameters)`

Initialize mixed parameter space.

[View full source →](#method-mixedparameterspace-__init__)

##### `sample(self, n_samples, rng)`

Sample from mixed parameter space.

[View full source →](#method-mixedparameterspace-sample)

##### `validate(self, parameters)`

Validate mixed parameters.

[View full source →](#method-mixedparameterspace-validate)

##### `clip(self, parameters)`

Clip mixed parameters.

[View full source →](#method-mixedparameterspace-clip)

##### `dimensions(self)`

Number of parameters.

[View full source →](#method-mixedparameterspace-dimensions)

##### `bounds(self)`

Parameter bounds.

[View full source →](#method-mixedparameterspace-bounds)

---

### `ParameterBounds`

Helper class for parameter bounds management.

#### Source Code

```{literalinclude} ../../../src/optimization/core/parameters.py
:language: python
:pyobject: ParameterBounds
:linenos:
```

#### Methods (4)

##### `__init__(self, lower, upper, names)`

Initialize parameter bounds.

[View full source →](#method-parameterbounds-__init__)

##### `to_parameter_space(self)`

Convert to continuous parameter space.

[View full source →](#method-parameterbounds-to_parameter_space)

##### `scale_to_unit(self, parameters)`

Scale parameters to unit cube [0,1]^n.

[View full source →](#method-parameterbounds-scale_to_unit)

##### `scale_from_unit(self, unit_parameters)`

Scale parameters from unit cube to original bounds.

[View full source →](#method-parameterbounds-scale_from_unit)

---

### `ParameterMapping`

Maps between different parameter representations.

#### Source Code

```{literalinclude} ../../../src/optimization/core/parameters.py
:language: python
:pyobject: ParameterMapping
:linenos:
```

#### Methods (3)

##### `__init__(self, parameter_space)`

Initialize parameter mapping.

[View full source →](#method-parametermapping-__init__)

##### `to_dict(self, parameters)`

Convert parameter array to dictionary.

[View full source →](#method-parametermapping-to_dict)

##### `from_dict(self, param_dict)`

Convert parameter dictionary to array.

[View full source →](#method-parametermapping-from_dict)

---

### `ParameterValidator`

Validates optimization parameters.

#### Source Code

```{literalinclude} ../../../src/optimization/core/parameters.py
:language: python
:pyobject: ParameterValidator
:linenos:
```

#### Methods (3)

##### `__init__(self, parameter_space)`

Initialize parameter validator.

[View full source →](#method-parametervalidator-__init__)

##### `validate_single(self, parameters)`

Validate single parameter vector.

[View full source →](#method-parametervalidator-validate_single)

##### `validate_batch(self, parameters)`

Validate batch of parameter vectors.

[View full source →](#method-parametervalidator-validate_batch)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from abc import ABC, abstractmethod`
- `from typing import Any, Dict, List, Optional, Tuple, Union`
- `import numpy as np`
- `from .interfaces import ParameterSpace`
