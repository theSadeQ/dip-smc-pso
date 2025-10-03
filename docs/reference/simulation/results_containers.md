# simulation.results.containers

**Source:** `src\simulation\results\containers.py`

## Module Overview

Result container implementations for simulation data.

## Complete Source Code

```{literalinclude} ../../../src/simulation/results/containers.py
:language: python
:linenos:
```

---

## Classes

### `StandardResultContainer`

**Inherits from:** `ResultContainer`

Standard result container for single simulations.

#### Source Code

```{literalinclude} ../../../src/simulation/results/containers.py
:language: python
:pyobject: StandardResultContainer
:linenos:
```

#### Methods (5)

##### `__init__(self)`

Initialize standard result container.

[View full source →](#method-standardresultcontainer-__init__)

##### `add_trajectory(self, states, times)`

Add trajectory data to container.

[View full source →](#method-standardresultcontainer-add_trajectory)

##### `get_states(self)`

Get state trajectories.

[View full source →](#method-standardresultcontainer-get_states)

##### `get_times(self)`

Get time vectors.

[View full source →](#method-standardresultcontainer-get_times)

##### `export(self, format_type, filepath)`

Export results to specified format.

[View full source →](#method-standardresultcontainer-export)

---

### `BatchResultContainer`

**Inherits from:** `ResultContainer`

Batch result container for multiple simulations.

#### Source Code

```{literalinclude} ../../../src/simulation/results/containers.py
:language: python
:pyobject: BatchResultContainer
:linenos:
```

#### Methods (6)

##### `__init__(self)`

Initialize batch result container.

[View full source →](#method-batchresultcontainer-__init__)

##### `add_trajectory(self, states, times)`

Add trajectory data to batch container.

[View full source →](#method-batchresultcontainer-add_trajectory)

##### `get_states(self, batch_index)`

Get state trajectories for specific batch or all batches.

[View full source →](#method-batchresultcontainer-get_states)

##### `get_times(self, batch_index)`

Get time vectors for specific batch or all batches.

[View full source →](#method-batchresultcontainer-get_times)

##### `export(self, format_type, filepath)`

Export batch results to specified format.

[View full source →](#method-batchresultcontainer-export)

##### `get_batch_count(self)`

Get number of batches.

[View full source →](#method-batchresultcontainer-get_batch_count)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Any, Dict, List, Optional`
- `import numpy as np`
- `from ..core.interfaces import ResultContainer`
