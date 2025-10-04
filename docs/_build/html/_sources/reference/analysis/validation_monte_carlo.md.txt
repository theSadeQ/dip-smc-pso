# analysis.validation.monte_carlo

**Source:** `src\analysis\validation\monte_carlo.py`

## Module Overview

Monte Carlo analysis tools for validation and uncertainty quantification.

This module provides comprehensive Monte Carlo simulation capabilities for
analyzing system behavior under uncertainty, validating controller performance,
and quantifying confidence in analysis results.

## Complete Source Code

```{literalinclude} ../../../src/analysis/validation/monte_carlo.py
:language: python
:linenos:
```

---

## Classes

### `MonteCarloConfig`

Configuration for Monte Carlo analysis.

#### Source Code

```{literalinclude} ../../../src/analysis/validation/monte_carlo.py
:language: python
:pyobject: MonteCarloConfig
:linenos:
```

---

### `MonteCarloAnalyzer`

**Inherits from:** `StatisticalValidator`

Monte Carlo analyzer for uncertainty quantification and validation.

#### Source Code

```{literalinclude} ../../../src/analysis/validation/monte_carlo.py
:language: python
:pyobject: MonteCarloAnalyzer
:linenos:
```

#### Methods (32)

##### `__init__(self, config)`

Initialize Monte Carlo analyzer.

[View full source →](#method-montecarloanalyzer-__init__)

##### `validation_methods(self)`

List of validation methods supported.

[View full source →](#method-montecarloanalyzer-validation_methods)

##### `validate(self, data)`

Perform Monte Carlo validation analysis.

[View full source →](#method-montecarloanalyzer-validate)

##### `_perform_monte_carlo_simulation(self, simulation_function, parameter_distributions)`

Perform Monte Carlo simulation.

[View full source →](#method-montecarloanalyzer-_perform_monte_carlo_simulation)

##### `_generate_parameter_samples(self, parameter_distributions)`

Generate parameter samples according to specified distributions.

[View full source →](#method-montecarloanalyzer-_generate_parameter_samples)

##### `_random_sampling(self, parameter_distributions)`

Generate random samples.

[View full source →](#method-montecarloanalyzer-_random_sampling)

##### `_latin_hypercube_sampling(self, parameter_distributions)`

Latin Hypercube Sampling for better space coverage.

[View full source →](#method-montecarloanalyzer-_latin_hypercube_sampling)

##### `_sobol_sampling(self, parameter_distributions)`

Sobol sequence sampling (simplified implementation).

[View full source →](#method-montecarloanalyzer-_sobol_sampling)

##### `_halton_sampling(self, parameter_distributions)`

Halton sequence sampling.

[View full source →](#method-montecarloanalyzer-_halton_sampling)

##### `_sample_from_distribution(self, distribution_info)`

Sample from a distribution specification.

[View full source →](#method-montecarloanalyzer-_sample_from_distribution)

##### `_inverse_transform_sample(self, uniform_value, distribution_info)`

Transform uniform sample to target distribution using inverse CDF.

[View full source →](#method-montecarloanalyzer-_inverse_transform_sample)

##### `_van_der_corput_sequence(self, n, base)`

Generate van der Corput sequence value.

[View full source →](#method-montecarloanalyzer-_van_der_corput_sequence)

##### `_generate_antithetic_variate(self, value, distribution_info)`

Generate antithetic variate for variance reduction.

[View full source →](#method-montecarloanalyzer-_generate_antithetic_variate)

##### `_run_simulations(self, simulation_function, parameter_samples)`

Run Monte Carlo simulations.

[View full source →](#method-montecarloanalyzer-_run_simulations)

##### `_run_simulations_sequential(self, simulation_function, parameter_samples)`

Run simulations sequentially.

[View full source →](#method-montecarloanalyzer-_run_simulations_sequential)

##### `_run_simulations_parallel(self, simulation_function, parameter_samples)`

Run simulations in parallel.

[View full source →](#method-montecarloanalyzer-_run_simulations_parallel)

##### `_safe_simulation_wrapper(self, simulation_function, params)`

Wrapper for safe simulation execution.

[View full source →](#method-montecarloanalyzer-_safe_simulation_wrapper)

##### `_analyze_simulation_results(self, results)`

Analyze Monte Carlo simulation results.

[View full source →](#method-montecarloanalyzer-_analyze_simulation_results)

##### `_compute_statistical_summary(self, values)`

Compute comprehensive statistical summary.

[View full source →](#method-montecarloanalyzer-_compute_statistical_summary)

##### `_analyze_convergence(self, results)`

Analyze Monte Carlo convergence.

[View full source →](#method-montecarloanalyzer-_analyze_convergence)

##### `_analyze_data_with_monte_carlo(self, data)`

Analyze existing data using Monte Carlo methods.

[View full source →](#method-montecarloanalyzer-_analyze_data_with_monte_carlo)

##### `_perform_bootstrap_analysis(self, data)`

Perform bootstrap analysis.

[View full source →](#method-montecarloanalyzer-_perform_bootstrap_analysis)

##### `_bootstrap_analysis(self, values)`

Perform bootstrap resampling analysis.

[View full source →](#method-montecarloanalyzer-_bootstrap_analysis)

##### `_subsampling_analysis(self, values)`

Perform subsampling analysis.

[View full source →](#method-montecarloanalyzer-_subsampling_analysis)

##### `_perform_sensitivity_analysis(self, simulation_function, parameter_distributions)`

Perform sensitivity analysis.

[View full source →](#method-montecarloanalyzer-_perform_sensitivity_analysis)

##### `_simple_sensitivity_analysis(self, simulation_function, parameter_distributions)`

Simple one-at-a-time sensitivity analysis.

[View full source →](#method-montecarloanalyzer-_simple_sensitivity_analysis)

##### `_sobol_sensitivity_analysis(self, simulation_function, parameter_distributions)`

Simplified Sobol sensitivity analysis.

[View full source →](#method-montecarloanalyzer-_sobol_sensitivity_analysis)

##### `_morris_sensitivity_analysis(self, simulation_function, parameter_distributions)`

Simplified Morris sensitivity analysis.

[View full source →](#method-montecarloanalyzer-_morris_sensitivity_analysis)

##### `_analyze_distributions(self, data)`

Analyze and fit distributions to data.

[View full source →](#method-montecarloanalyzer-_analyze_distributions)

##### `_perform_risk_analysis(self, data)`

Perform risk analysis including tail risk assessment.

[View full source →](#method-montecarloanalyzer-_perform_risk_analysis)

##### `_extreme_value_analysis(self, values)`

Perform extreme value analysis.

[View full source →](#method-montecarloanalyzer-_extreme_value_analysis)

##### `_generate_validation_summary(self, results)`

Generate validation summary.

[View full source →](#method-montecarloanalyzer-_generate_validation_summary)

---

## Functions

### `create_monte_carlo_analyzer(config)`

Factory function to create Monte Carlo analyzer.

Parameters
----------
config : Dict[str, Any], optional
    Configuration parameters

Returns
-------
MonteCarloAnalyzer
    Configured Monte Carlo analyzer

#### Source Code

```{literalinclude} ../../../src/analysis/validation/monte_carlo.py
:language: python
:pyobject: create_monte_carlo_analyzer
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Dict, List, Optional, Tuple, Any, Union, Callable`
- `import numpy as np`
- `from scipy import stats`
- `import warnings`
- `from dataclasses import dataclass, field`
- `from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor`
- `import multiprocessing`
- `from functools import partial`
- `from ..core.interfaces import StatisticalValidator, AnalysisResult, AnalysisStatus, DataProtocol`

*... and 1 more*
