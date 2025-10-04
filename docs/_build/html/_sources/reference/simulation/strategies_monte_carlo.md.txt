# simulation.strategies.monte_carlo

**Source:** `src\simulation\strategies\monte_carlo.py`

## Module Overview

Monte Carlo simulation strategy for statistical analysis.

## Complete Source Code

```{literalinclude} ../../../src/simulation/strategies/monte_carlo.py
:language: python
:linenos:
```

---

## Classes

### `MonteCarloStrategy`

**Inherits from:** `SimulationStrategy`

Monte Carlo simulation strategy for statistical analysis.

#### Source Code

```{literalinclude} ../../../src/simulation/strategies/monte_carlo.py
:language: python
:pyobject: MonteCarloStrategy
:linenos:
```

#### Methods (7)

##### `__init__(self, n_samples, parallel, max_workers)`

Initialize Monte Carlo strategy.

[View full source →](#method-montecarlostrategy-__init__)

##### `analyze(self, simulation_fn, parameters)`

Perform Monte Carlo analysis.

[View full source →](#method-montecarlostrategy-analyze)

##### `_generate_samples(self, distributions)`

Generate Monte Carlo parameter samples.

[View full source →](#method-montecarlostrategy-_generate_samples)

##### `_run_parallel_simulations(self, simulation_fn, samples, fixed_params)`

Run simulations in parallel.

[View full source →](#method-montecarlostrategy-_run_parallel_simulations)

##### `_run_sequential_simulations(self, simulation_fn, samples, fixed_params)`

Run simulations sequentially.

[View full source →](#method-montecarlostrategy-_run_sequential_simulations)

##### `_analyze_results(self, results, samples)`

Analyze Monte Carlo results.

[View full source →](#method-montecarlostrategy-_analyze_results)

##### `_extract_metrics(self, results)`

Extract metrics from simulation results.

[View full source →](#method-montecarlostrategy-_extract_metrics)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Any, Callable, Dict, List, Optional`
- `import numpy as np`
- `from ..core.interfaces import SimulationStrategy`
- `from ..orchestrators.parallel import ParallelOrchestrator`
