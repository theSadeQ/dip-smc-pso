# simulation.core.state_space

**Source:** `src\simulation\core\state_space.py`

## Module Overview

State-space representation utilities for simulation framework.

## Complete Source Code

```{literalinclude} ../../../src/simulation/core/state_space.py
:language: python
:linenos:
```

---

## Classes

### `StateSpaceUtilities`

Utilities for state-space system representations and manipulations.

#### Source Code

```{literalinclude} ../../../src/simulation/core/state_space.py
:language: python
:pyobject: StateSpaceUtilities
:linenos:
```

#### Methods (6)

##### `validate_state_dimensions(state, expected_dim)`

Validate state vector dimensions.

[View full source →](#method-statespaceutilities-validate_state_dimensions)

##### `normalize_state_batch(states)`

Normalize state array to consistent batch format.

[View full source →](#method-statespaceutilities-normalize_state_batch)

##### `extract_state_components(state, indices)`

Extract named state components from state vector.

[View full source →](#method-statespaceutilities-extract_state_components)

##### `compute_state_bounds(states, percentile)`

Compute state bounds from trajectory data.

[View full source →](#method-statespaceutilities-compute_state_bounds)

##### `compute_energy(state, mass_matrix)`

Compute system energy from state vector.

[View full source →](#method-statespaceutilities-compute_energy)

##### `linearize_about_equilibrium(dynamics_fn, equilibrium_state, equilibrium_control, epsilon)`

Linearize dynamics about an equilibrium point.

[View full source →](#method-statespaceutilities-linearize_about_equilibrium)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Any, Dict, List, Optional, Tuple, Union`
- `import numpy as np`
