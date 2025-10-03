# analysis.performance.robustness

**Source:** `src\analysis\performance\robustness.py`

## Module Overview

Robustness analysis tools for control systems.

This module provides comprehensive robustness analysis capabilities including
sensitivity analysis, uncertainty quantification, and robust performance metrics.

## Complete Source Code

```{literalinclude} ../../../src/analysis/performance/robustness.py
:language: python
:linenos:
```

---

## Classes

### `RobustnessAnalysisConfig`

Configuration for robustness analysis.

#### Source Code

```{literalinclude} ../../../src/analysis/performance/robustness.py
:language: python
:pyobject: RobustnessAnalysisConfig
:linenos:
```

---

### `UncertaintyModel`

Model for system uncertainties.

#### Source Code

```{literalinclude} ../../../src/analysis/performance/robustness.py
:language: python
:pyobject: UncertaintyModel
:linenos:
```

---

### `RobustnessAnalyzer`

**Inherits from:** `PerformanceAnalyzer`

Comprehensive robustness analysis for control systems.

#### Source Code

```{literalinclude} ../../../src/analysis/performance/robustness.py
:language: python
:pyobject: RobustnessAnalyzer
:linenos:
```

#### Methods (34)

##### `__init__(self, config)`

Initialize robustness analyzer.

[View full source →](#method-robustnessanalyzer-__init__)

##### `analyzer_name(self)`

Name of the analyzer.

[View full source →](#method-robustnessanalyzer-analyzer_name)

##### `required_data_fields(self)`

Required data fields for analysis.

[View full source →](#method-robustnessanalyzer-required_data_fields)

##### `analyze(self, data)`

Perform comprehensive robustness analysis.

[View full source →](#method-robustnessanalyzer-analyze)

##### `_perform_sensitivity_analysis(self, data)`

Perform sensitivity analysis.

[View full source →](#method-robustnessanalyzer-_perform_sensitivity_analysis)

##### `_analyze_parameter_sensitivity(self, data, parameter_ranges)`

Analyze sensitivity to parameter variations.

[View full source →](#method-robustnessanalyzer-_analyze_parameter_sensitivity)

##### `_analyze_initial_condition_sensitivity(self, data)`

Analyze sensitivity to initial conditions.

[View full source →](#method-robustnessanalyzer-_analyze_initial_condition_sensitivity)

##### `_analyze_disturbance_sensitivity(self, data)`

Analyze sensitivity to external disturbances.

[View full source →](#method-robustnessanalyzer-_analyze_disturbance_sensitivity)

##### `_perform_monte_carlo_analysis(self, data)`

Perform Monte Carlo robustness analysis.

[View full source →](#method-robustnessanalyzer-_perform_monte_carlo_analysis)

##### `_perform_worst_case_analysis(self, data)`

Perform worst-case performance analysis.

[View full source →](#method-robustnessanalyzer-_perform_worst_case_analysis)

##### `_analyze_structured_uncertainties(self, data, uncertainty_models)`

Analyze structured uncertainties.

[View full source →](#method-robustnessanalyzer-_analyze_structured_uncertainties)

##### `_compute_robustness_metrics(self, data)`

Compute various robustness metrics.

[View full source →](#method-robustnessanalyzer-_compute_robustness_metrics)

##### `_perform_statistical_robustness_analysis(self, data)`

Perform statistical robustness analysis.

[View full source →](#method-robustnessanalyzer-_perform_statistical_robustness_analysis)

##### `_analyze_performance_degradation(self, data)`

Analyze performance degradation under uncertainties.

[View full source →](#method-robustnessanalyzer-_analyze_performance_degradation)

##### `_default_performance_function(self, data)`

Default performance function (RMS of first state).

[View full source →](#method-robustnessanalyzer-_default_performance_function)

##### `_perturb_system_parameter(self, system_matrices, param_name, perturbation)`

Perturb a system parameter (simplified).

[View full source →](#method-robustnessanalyzer-_perturb_system_parameter)

##### `_simulate_perturbed_system(self, data, perturbed_matrices)`

Simulate system with perturbed parameters (placeholder).

[View full source →](#method-robustnessanalyzer-_simulate_perturbed_system)

##### `_simulate_with_initial_conditions(self, data, initial_conditions)`

Simulate with different initial conditions (placeholder).

[View full source →](#method-robustnessanalyzer-_simulate_with_initial_conditions)

##### `_apply_disturbance_to_data(self, data, disturbance)`

Apply disturbance to data (placeholder).

[View full source →](#method-robustnessanalyzer-_apply_disturbance_to_data)

##### `_generate_monte_carlo_samples(self, parameter_ranges, uncertainty_models)`

Generate Monte Carlo samples.

[View full source →](#method-robustnessanalyzer-_generate_monte_carlo_samples)

##### `_parallel_monte_carlo_evaluation(self, data, samples, performance_func)`

Evaluate Monte Carlo samples in parallel.

[View full source →](#method-robustnessanalyzer-_parallel_monte_carlo_evaluation)

##### `_sequential_monte_carlo_evaluation(self, data, samples, performance_func)`

Evaluate Monte Carlo samples sequentially.

[View full source →](#method-robustnessanalyzer-_sequential_monte_carlo_evaluation)

##### `_compute_monte_carlo_statistics(self, results)`

Compute statistics from Monte Carlo results.

[View full source →](#method-robustnessanalyzer-_compute_monte_carlo_statistics)

##### `_analyze_performance_probabilities(self, results)`

Analyze performance probabilities.

[View full source →](#method-robustnessanalyzer-_analyze_performance_probabilities)

##### `_compute_confidence_intervals(self, results)`

Compute confidence intervals.

[View full source →](#method-robustnessanalyzer-_compute_confidence_intervals)

##### `_grid_search_worst_case(self, data, parameter_ranges, performance_func, grid_points)`

Grid search for worst-case performance.

[View full source →](#method-robustnessanalyzer-_grid_search_worst_case)

##### `_vertex_analysis(self, data, parameter_ranges, performance_func)`

Analyze performance at parameter range vertices.

[View full source →](#method-robustnessanalyzer-_vertex_analysis)

##### `_analyze_single_uncertainty_model(self, data, model)`

Analyze a single uncertainty model.

[View full source →](#method-robustnessanalyzer-_analyze_single_uncertainty_model)

##### `_compute_stability_robustness(self, system_matrices)`

Compute stability robustness metrics.

[View full source →](#method-robustnessanalyzer-_compute_stability_robustness)

##### `_compute_performance_robustness(self, data)`

Compute performance robustness metrics.

[View full source →](#method-robustnessanalyzer-_compute_performance_robustness)

##### `_compute_control_effort_robustness(self, data)`

Compute control effort robustness metrics.

[View full source →](#method-robustnessanalyzer-_compute_control_effort_robustness)

##### `_bootstrap_robustness_analysis(self, data, performance_func)`

Bootstrap analysis for robustness confidence intervals.

[View full source →](#method-robustnessanalyzer-_bootstrap_robustness_analysis)

##### `_perform_robustness_hypothesis_tests(self, data)`

Perform hypothesis tests for robustness.

[View full source →](#method-robustnessanalyzer-_perform_robustness_hypothesis_tests)

##### `_generate_robustness_assessment(self, results)`

Generate overall robustness assessment.

[View full source →](#method-robustnessanalyzer-_generate_robustness_assessment)

---

## Functions

### `create_robustness_analyzer(config)`

Factory function to create robustness analyzer.

Parameters
----------
config : Dict[str, Any], optional
    Configuration parameters

Returns
-------
RobustnessAnalyzer
    Configured robustness analyzer

#### Source Code

```{literalinclude} ../../../src/analysis/performance/robustness.py
:language: python
:pyobject: create_robustness_analyzer
:linenos:
```

---

### `create_uncertainty_model(name, uncertainty_type, distribution)`

Factory function to create uncertainty models.

Parameters
----------
name : str
    Name of the uncertainty
uncertainty_type : str
    Type of uncertainty ('parametric', 'additive', 'multiplicative', 'structured')
distribution : str
    Distribution type ('normal', 'uniform', 'beta', 'custom')
**parameters
    Distribution parameters

Returns
-------
UncertaintyModel
    Configured uncertainty model

#### Source Code

```{literalinclude} ../../../src/analysis/performance/robustness.py
:language: python
:pyobject: create_uncertainty_model
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Dict, List, Optional, Tuple, Any, Union, Callable`
- `import numpy as np`
- `from scipy import linalg, stats`
- `import warnings`
- `from dataclasses import dataclass, field`
- `from concurrent.futures import ProcessPoolExecutor`
- `import multiprocessing`
- `from ..core.interfaces import PerformanceAnalyzer, AnalysisResult, AnalysisStatus, DataProtocol`
- `from ..core.data_structures import MetricResult, PerformanceMetrics, ConfidenceInterval, StatisticalTestResult`
