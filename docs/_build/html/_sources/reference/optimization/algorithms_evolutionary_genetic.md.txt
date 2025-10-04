# optimization.algorithms.evolutionary.genetic

**Source:** `src\optimization\algorithms\evolutionary\genetic.py`

## Module Overview

Genetic Algorithm implementation for control parameter optimization.

## Complete Source Code

```{literalinclude} ../../../src/optimization/algorithms/evolutionary/genetic.py
:language: python
:linenos:
```

---

## Classes

### `GeneticAlgorithmConfig`

Configuration for Genetic Algorithm.

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/evolutionary/genetic.py
:language: python
:pyobject: GeneticAlgorithmConfig
:linenos:
```

---

### `Individual`

Individual in the genetic algorithm population.

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/evolutionary/genetic.py
:language: python
:pyobject: Individual
:linenos:
```

#### Methods (3)

##### `__init__(self, genes, fitness)`

[View full source →](#method-individual-__init__)

##### `copy(self)`

Create a copy of the individual.

[View full source →](#method-individual-copy)

##### `__str__(self)`

[View full source →](#method-individual-__str__)

---

### `GeneticAlgorithm`

**Inherits from:** `OptimizationAlgorithm`

Genetic Algorithm for parameter optimization.

A population-based evolutionary algorithm that uses selection, crossover,
and mutation operators to evolve a population of candidate solutions.

Features:
- Multiple selection methods (tournament, roulette, rank)
- Various crossover operators (uniform, single-point, arithmetic)
- Adaptive mutation strategies
- Elitist preservation
- Diversity maintenance
- Parallel fitness evaluation

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/evolutionary/genetic.py
:language: python
:pyobject: GeneticAlgorithm
:linenos:
```

#### Methods (30)

##### `__init__(self, config)`

Initialize Genetic Algorithm.

[View full source →](#method-geneticalgorithm-__init__)

##### `optimize(self, problem, parameter_space)`

Run genetic algorithm optimization.

[View full source →](#method-geneticalgorithm-optimize)

##### `_initialize_population(self)`

Initialize the population randomly.

[View full source →](#method-geneticalgorithm-_initialize_population)

##### `_evaluate_population(self)`

Evaluate fitness for all individuals in population.

[View full source →](#method-geneticalgorithm-_evaluate_population)

##### `_evaluate_population_serial(self)`

Evaluate population serially.

[View full source →](#method-geneticalgorithm-_evaluate_population_serial)

##### `_evaluate_population_parallel(self)`

Evaluate population in parallel.

[View full source →](#method-geneticalgorithm-_evaluate_population_parallel)

##### `_safe_evaluate(self, genes)`

Safe evaluation wrapper for parallel processing.

[View full source →](#method-geneticalgorithm-_safe_evaluate)

##### `_create_new_generation(self)`

Create new generation using selection, crossover, and mutation.

[View full source →](#method-geneticalgorithm-_create_new_generation)

##### `_select_elite(self, count)`

Select elite individuals (best fitness).

[View full source →](#method-geneticalgorithm-_select_elite)

##### `_select_individual(self)`

Select individual based on selection method.

[View full source →](#method-geneticalgorithm-_select_individual)

##### `_tournament_selection(self)`

Tournament selection.

[View full source →](#method-geneticalgorithm-_tournament_selection)

##### `_roulette_selection(self)`

Roulette wheel selection.

[View full source →](#method-geneticalgorithm-_roulette_selection)

##### `_rank_selection(self)`

Rank-based selection.

[View full source →](#method-geneticalgorithm-_rank_selection)

##### `_crossover(self, parent1, parent2)`

Perform crossover between two parents.

[View full source →](#method-geneticalgorithm-_crossover)

##### `_uniform_crossover(self, parent1, parent2)`

Uniform crossover - each gene has 50% chance of coming from either parent.

[View full source →](#method-geneticalgorithm-_uniform_crossover)

##### `_single_point_crossover(self, parent1, parent2)`

Single-point crossover.

[View full source →](#method-geneticalgorithm-_single_point_crossover)

##### `_arithmetic_crossover(self, parent1, parent2)`

Arithmetic crossover - weighted average of parents.

[View full source →](#method-geneticalgorithm-_arithmetic_crossover)

##### `_mutate(self, individual)`

Mutate an individual.

[View full source →](#method-geneticalgorithm-_mutate)

##### `_gaussian_mutation(self, individual)`

Gaussian mutation - add normally distributed noise.

[View full source →](#method-geneticalgorithm-_gaussian_mutation)

##### `_uniform_mutation(self, individual)`

Uniform mutation - replace with random value in range.

[View full source →](#method-geneticalgorithm-_uniform_mutation)

##### `_polynomial_mutation(self, individual)`

Polynomial mutation.

[View full source →](#method-geneticalgorithm-_polynomial_mutation)

##### `_update_algorithm_state(self)`

Update algorithm state after each generation.

[View full source →](#method-geneticalgorithm-_update_algorithm_state)

##### `_update_best_individual(self)`

Update the best individual found so far.

[View full source →](#method-geneticalgorithm-_update_best_individual)

##### `_calculate_diversity(self)`

Calculate population diversity.

[View full source →](#method-geneticalgorithm-_calculate_diversity)

##### `_update_adaptive_parameters(self)`

Update adaptive algorithm parameters.

[View full source →](#method-geneticalgorithm-_update_adaptive_parameters)

##### `_check_convergence(self)`

Check if algorithm has converged.

[View full source →](#method-geneticalgorithm-_check_convergence)

##### `_create_result(self)`

Create optimization result.

[View full source →](#method-geneticalgorithm-_create_result)

##### `get_population_statistics(self)`

Get statistics about current population.

[View full source →](#method-geneticalgorithm-get_population_statistics)

##### `_estimate_convergence_rate(self)`

Estimate convergence rate from fitness history.

[View full source →](#method-geneticalgorithm-_estimate_convergence_rate)

##### `_calculate_selection_pressure(self)`

Calculate selection pressure in population.

[View full source →](#method-geneticalgorithm-_calculate_selection_pressure)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Any, Dict, List, Optional, Callable, Tuple, Union`
- `import numpy as np`
- `import warnings`
- `from dataclasses import dataclass`
- `from concurrent.futures import ProcessPoolExecutor`
- `import multiprocessing as mp`
- `from ..base import OptimizationAlgorithm`
- `from ...core.interfaces import OptimizationProblem, ParameterSpace, OptimizationResult`
- `from ...core.parameters import ContinuousParameterSpace`

*... and 1 more*
