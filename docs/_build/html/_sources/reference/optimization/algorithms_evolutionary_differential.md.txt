# optimization.algorithms.evolutionary.differential

**Source:** `src\optimization\algorithms\evolutionary\differential.py`

## Module Overview

Differential Evolution optimization algorithm.

## Complete Source Code

```{literalinclude} ../../../src/optimization/algorithms/evolutionary/differential.py
:language: python
:linenos:
```

---

## Classes

### `DifferentialEvolution`

**Inherits from:** `PopulationBasedOptimizer`

Differential Evolution algorithm for global optimization.

DE is a robust evolutionary algorithm particularly effective for
continuous optimization problems with multimodal landscapes.

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/evolutionary/differential.py
:language: python
:pyobject: DifferentialEvolution
:linenos:
```

#### Methods (16)

##### `__init__(self, parameter_space, population_size, mutation_factor, crossover_probability, strategy, max_iterations, tolerance, adaptive_parameters)`

Initialize Differential Evolution optimizer.

[View full source →](#method-differentialevolution-__init__)

##### `algorithm_name(self)`

Algorithm name.

[View full source →](#method-differentialevolution-algorithm_name)

##### `supports_constraints(self)`

DE can handle constraints through penalty methods.

[View full source →](#method-differentialevolution-supports_constraints)

##### `supports_bounds(self)`

DE naturally supports parameter bounds.

[View full source →](#method-differentialevolution-supports_bounds)

##### `optimize(self, problem)`

Perform DE optimization.

[View full source →](#method-differentialevolution-optimize)

##### `initialize_population(self, rng)`

Initialize population randomly within bounds.

[View full source →](#method-differentialevolution-initialize_population)

##### `update_population(self, population, fitness)`

Update population (used by base class interface).

[View full source →](#method-differentialevolution-update_population)

##### `_create_trial_population(self, rng)`

Create trial population using DE mutation and crossover.

[View full source →](#method-differentialevolution-_create_trial_population)

##### `_mutate(self, target_index, rng)`

Apply DE mutation strategy.

[View full source →](#method-differentialevolution-_mutate)

##### `_crossover(self, target, mutant, rng)`

Apply binomial crossover.

[View full source →](#method-differentialevolution-_crossover)

##### `_select_random_indices(self, exclude, count, rng)`

Select random indices excluding the target index.

[View full source →](#method-differentialevolution-_select_random_indices)

##### `_selection(self, trial_population, trial_fitness)`

Selection between current and trial populations.

[View full source →](#method-differentialevolution-_selection)

##### `_update_best(self)`

Update best individual and fitness.

[View full source →](#method-differentialevolution-_update_best)

##### `_adapt_parameters(self, iteration, max_iterations)`

Adapt F and CR parameters during evolution.

[View full source →](#method-differentialevolution-_adapt_parameters)

##### `_apply_constraint_penalties(self, fitness, population, problem)`

Apply constraint penalties to fitness values.

[View full source →](#method-differentialevolution-_apply_constraint_penalties)

##### `get_population_statistics(self)`

Get detailed population statistics.

[View full source →](#method-differentialevolution-get_population_statistics)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import numpy as np`
- `from typing import Any, Dict, Optional, Tuple`
- `import logging`
- `from ...core.interfaces import PopulationBasedOptimizer, OptimizationProblem, OptimizationResult, ConvergenceStatus, ParameterSpace`
