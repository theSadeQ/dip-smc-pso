# analysis.validation.statistical_benchmarks

**Source:** `src\analysis\validation\statistical_benchmarks.py`

## Module Overview

Statistical benchmarking utilities for the Double Inverted Pendulum project.

This is the refactored version using modular architecture while maintaining
full backward compatibility with the original statistical_benchmarks.py.

The module now delegates to specialized submodules:
- **metrics/**: Performance metric calculations
- **core/**: Trial execution and orchestration
- **statistics/**: Confidence interval analysis

This refactoring provides:
* **Modularity**: Clear separation of concerns
* **Extensibility**: Easy addition of new metrics or analysis methods
* **Maintainability**: Smaller, focused modules
* **Testability**: Individual components can be tested in isolation
* **Compatibility**: Original API preserved for existing code

Usage remains identical to the original:
    from src.benchmarks.statistical_benchmarks_v2 import run_trials

    metrics_list, ci_results = run_trials(controller_factory, cfg)

## Complete Source Code

```{literalinclude} ../../../src/analysis/validation/statistical_benchmarks.py
:language: python
:linenos:
```

---

## Classes

### `StatisticalBenchmarks`

Statistical benchmarking utilities for control system analysis.

This class provides a unified interface for running statistical benchmarks,
comparing controller performance, and analyzing experimental results.

#### Source Code

```{literalinclude} ../../../src/analysis/validation/statistical_benchmarks.py
:language: python
:pyobject: StatisticalBenchmarks
:linenos:
```

#### Methods (3)

##### `__init__(self, random_seed)`

Initialize statistical benchmarks.

[View full source →](#method-statisticalbenchmarks-__init__)

##### `run_benchmark(self, benchmark_function, configurations, repetitions)`

Run benchmark across multiple configurations.

[View full source →](#method-statisticalbenchmarks-run_benchmark)

##### `compare_configurations(self, results, metric_name)`

Compare multiple configuration results for a specific metric.

[View full source →](#method-statisticalbenchmarks-compare_configurations)

---

## Functions

### `compute_metrics(t, x, u, sigma, max_force)`

Compute performance metrics for a batch of trajectories.

This function maintains exact compatibility with the original
implementation while delegating to the new modular structure.

Parameters
----------
t : np.ndarray
    One‑dimensional array of time stamps of length ``N+1``.
x : np.ndarray
    Array of shape ``(B, N+1, S)`` containing the state trajectories for
    ``B`` particles over ``S`` state dimensions.
u : np.ndarray
    Array of shape ``(B, N)`` containing the control inputs.
sigma : np.ndarray
    Array of shape ``(B, N)`` containing sliding variables or auxiliary
    outputs. (Not used in basic metrics but preserved for compatibility)
max_force : float
    Maximum allowable magnitude of the control input.  Used to count
    constraint violations.

Returns
-------
dict
    Mapping of metric names to scalar values.  Each metric is averaged
    across the batch dimension.

#### Source Code

```{literalinclude} ../../../src/analysis/validation/statistical_benchmarks.py
:language: python
:pyobject: compute_metrics
:linenos:
```

---

### `run_trials(controller_factory, cfg, n_trials, seed, randomise_physics, noise_std)`

Run multiple simulations and return per‑trial metrics with confidence intervals.

This function maintains exact compatibility with the original implementation
while using the new modular architecture under the hood.

The function executes ``n_trials`` independent simulations of the
double inverted pendulum under the supplied controller factory and
configuration.  For each trial it collects performance metrics and
computes a 95 % confidence interval for the mean of each metric.  A
sample size of at least 25–30 trials is recommended to invoke the
Central Limit Theorem for skewed distributions.

Parameters
----------
controller_factory : Callable[[np.ndarray], Any]
    Factory function that returns a controller instance when provided
    with a gain vector.  The returned controller must define an
    ``n_gains`` attribute and may define ``max_force``.
cfg : Any
    Full configuration object (e.g., ``ConfigSchema``) supplying
    physics and simulation parameters.  Only ``simulation.duration``
    and ``simulation.dt`` are required by this harness.
n_trials : int, optional
    Number of independent trials to run.  Defaults to 30.
seed : int, optional
    Base random seed used to initialise each trial.  Individual trials
    draw their seeds from a NumPy generator seeded with this value.
randomise_physics : bool, optional
    When True, randomly perturb the physical parameters between trials.
    Not implemented in this harness; reserved for future use.
noise_std : float, optional
    Standard deviation of additive Gaussian noise applied to the state
    trajectories before metric computation.

Returns
-------
list of dict, dict
    A list containing the raw metrics for each trial and a dictionary
    mapping metric names to tuples ``(mean, ci)`` where ``ci`` is
    half the width of the 95 % confidence interval.

#### Source Code

```{literalinclude} ../../../src/analysis/validation/statistical_benchmarks.py
:language: python
:pyobject: run_trials
:linenos:
```

---

### `run_trials_with_advanced_statistics(controller_factory, cfg, n_trials, seed, confidence_level, use_bootstrap)`

Run trials with advanced statistical analysis.

This function extends the original capability with additional
statistical analysis options.

Parameters
----------
controller_factory, cfg, n_trials, seed :
    Same as run_trials()
confidence_level : float, optional
    Confidence level for intervals (default 0.95)
use_bootstrap : bool, optional
    Whether to use bootstrap confidence intervals
**kwargs :
    Additional arguments passed to trial runner

Returns
-------
list of dict, dict
    Metrics list and comprehensive statistical analysis results

#### Source Code

```{literalinclude} ../../../src/analysis/validation/statistical_benchmarks.py
:language: python
:pyobject: run_trials_with_advanced_statistics
:linenos:
```

---

### `compare_controllers(controller_factory_a, controller_factory_b, cfg, n_trials, seed)`

Compare two controllers using statistical analysis.

Parameters
----------
controller_factory_a, controller_factory_b : Callable
    Controller factories to compare
cfg : Any
    Configuration object
n_trials : int, optional
    Number of trials per controller
seed : int, optional
    Base random seed
**kwargs :
    Additional arguments

Returns
-------
dict
    Comprehensive comparison results

#### Source Code

```{literalinclude} ../../../src/analysis/validation/statistical_benchmarks.py
:language: python
:pyobject: compare_controllers
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Callable, Dict, Any, List, Tuple, Optional`
- `import numpy as np`
- `from .metrics import compute_basic_metrics`
- `from .core import run_multiple_trials, validate_trial_configuration`
- `from .statistics import compute_basic_confidence_intervals`
