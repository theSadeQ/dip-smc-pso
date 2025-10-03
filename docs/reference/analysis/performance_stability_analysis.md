# analysis.performance.stability_analysis

**Source:** `src\analysis\performance\stability_analysis.py`

## Module Overview

Stability analysis tools for control systems.

This module provides comprehensive stability analysis capabilities including
Lyapunov analysis, eigenvalue analysis, and stability margin computation.

## Complete Source Code

```{literalinclude} ../../../src/analysis/performance/stability_analysis.py
:language: python
:linenos:
```

---

## Classes

### `StabilityAnalysisConfig`

Configuration for stability analysis.

#### Source Code

```{literalinclude} ../../../src/analysis/performance/stability_analysis.py
:language: python
:pyobject: StabilityAnalysisConfig
:linenos:
```

---

### `StabilityAnalyzer`

**Inherits from:** `PerformanceAnalyzer`

Comprehensive stability analysis for linear and nonlinear systems.

#### Source Code

```{literalinclude} ../../../src/analysis/performance/stability_analysis.py
:language: python
:pyobject: StabilityAnalyzer
:linenos:
```

#### Methods (37)

##### `__init__(self, config)`

Initialize stability analyzer.

[View full source →](#method-stabilityanalyzer-__init__)

##### `analyzer_name(self)`

Name of the analyzer.

[View full source →](#method-stabilityanalyzer-analyzer_name)

##### `required_data_fields(self)`

Required data fields for analysis.

[View full source →](#method-stabilityanalyzer-required_data_fields)

##### `analyze(self, data)`

Perform comprehensive stability analysis.

[View full source →](#method-stabilityanalyzer-analyze)

##### `_analyze_empirical_stability(self, data)`

Analyze stability from simulation data.

[View full source →](#method-stabilityanalyzer-_analyze_empirical_stability)

##### `_analyze_linear_stability(self, system_matrices)`

Analyze stability of linear system.

[View full source →](#method-stabilityanalyzer-_analyze_linear_stability)

##### `_analyze_frequency_domain_stability(self, system_matrices)`

Analyze stability in frequency domain.

[View full source →](#method-stabilityanalyzer-_analyze_frequency_domain_stability)

##### `_analyze_robustness(self, system_matrices, uncertainties)`

Analyze robustness to parameter uncertainties.

[View full source →](#method-stabilityanalyzer-_analyze_robustness)

##### `_analyze_lyapunov_stability(self, data, system_matrices)`

Analyze Lyapunov stability.

[View full source →](#method-stabilityanalyzer-_analyze_lyapunov_stability)

##### `_analyze_bibo_stability(self, data)`

Analyze bounded-input bounded-output stability.

[View full source →](#method-stabilityanalyzer-_analyze_bibo_stability)

##### `_check_state_boundedness(self, states)`

Check if states remain bounded.

[View full source →](#method-stabilityanalyzer-_check_state_boundedness)

##### `_analyze_trajectory_convergence(self, data)`

Analyze trajectory convergence properties.

[View full source →](#method-stabilityanalyzer-_analyze_trajectory_convergence)

##### `_analyze_energy_dissipation(self, data)`

Analyze energy dissipation properties.

[View full source →](#method-stabilityanalyzer-_analyze_energy_dissipation)

##### `_compute_time_series_stability_indicators(self, data)`

Compute stability indicators from time series.

[View full source →](#method-stabilityanalyzer-_compute_time_series_stability_indicators)

##### `_analyze_eigenvalues(self, eigenvalues)`

Analyze eigenvalue properties for stability.

[View full source →](#method-stabilityanalyzer-_analyze_eigenvalues)

##### `_check_controllability(self, A, B)`

Check system controllability.

[View full source →](#method-stabilityanalyzer-_check_controllability)

##### `_check_observability(self, A, C)`

Check system observability.

[View full source →](#method-stabilityanalyzer-_check_observability)

##### `_compute_continuous_stability_margins(self, A)`

Compute stability margins for continuous-time systems.

[View full source →](#method-stabilityanalyzer-_compute_continuous_stability_margins)

##### `_analyze_discrete_stability(self, A)`

Analyze stability for discrete-time systems.

[View full source →](#method-stabilityanalyzer-_analyze_discrete_stability)

##### `_analyze_nyquist_stability(self, frequencies, H)`

Analyze stability using Nyquist criterion.

[View full source →](#method-stabilityanalyzer-_analyze_nyquist_stability)

##### `_analyze_bode_stability(self, frequencies, H)`

Analyze stability from Bode plots.

[View full source →](#method-stabilityanalyzer-_analyze_bode_stability)

##### `_compute_stability_margins(self, frequencies, H)`

Compute gain and phase margins.

[View full source →](#method-stabilityanalyzer-_compute_stability_margins)

##### `_estimate_growth_rate(self, signal)`

Estimate growth rate of a signal.

[View full source →](#method-stabilityanalyzer-_estimate_growth_rate)

##### `_estimate_convergence_rate(self, times, magnitude)`

Estimate convergence rate from trajectory magnitude.

[View full source →](#method-stabilityanalyzer-_estimate_convergence_rate)

##### `_analyze_asymptotic_behavior(self, times, magnitude)`

Analyze asymptotic behavior of trajectory.

[View full source →](#method-stabilityanalyzer-_analyze_asymptotic_behavior)

##### `_check_signal_boundedness(self, signal)`

Check if a signal is bounded.

[View full source →](#method-stabilityanalyzer-_check_signal_boundedness)

##### `_estimate_empirical_lyapunov_function(self, data)`

Estimate empirical Lyapunov function from data.

[View full source →](#method-stabilityanalyzer-_estimate_empirical_lyapunov_function)

##### `_analyze_analytical_lyapunov(self, A)`

Analyze Lyapunov stability analytically with robust numerical methods.

[View full source →](#method-stabilityanalyzer-_analyze_analytical_lyapunov)

##### `_solve_lyapunov_svd(self, A, Q, regularizer)`

Solve Lyapunov equation using SVD-based robust method.

[View full source →](#method-stabilityanalyzer-_solve_lyapunov_svd)

##### `_estimate_largest_lyapunov_exponent(self, states)`

Estimate largest Lyapunov exponent (simplified method).

[View full source →](#method-stabilityanalyzer-_estimate_largest_lyapunov_exponent)

##### `_compute_stability_index(self, states)`

Compute stability index based on variance growth.

[View full source →](#method-stabilityanalyzer-_compute_stability_index)

##### `_analyze_recurrence(self, states)`

Analyze recurrence properties (simplified).

[View full source →](#method-stabilityanalyzer-_analyze_recurrence)

##### `_compute_damping_ratio_from_eigenvalue(self, eigenvalue)`

Compute damping ratio from complex eigenvalue.

[View full source →](#method-stabilityanalyzer-_compute_damping_ratio_from_eigenvalue)

##### `_compute_robustness_margins(self, A, uncertainties)`

Compute robustness margins (simplified).

[View full source →](#method-stabilityanalyzer-_compute_robustness_margins)

##### `_compute_sensitivity_analysis(self, A)`

Compute sensitivity of eigenvalues to parameter changes.

[View full source →](#method-stabilityanalyzer-_compute_sensitivity_analysis)

##### `_monte_carlo_robustness(self, A, uncertainties, n_samples)`

Monte Carlo robustness analysis.

[View full source →](#method-stabilityanalyzer-_monte_carlo_robustness)

##### `_generate_overall_assessment(self, results)`

Generate overall stability assessment.

[View full source →](#method-stabilityanalyzer-_generate_overall_assessment)

---

## Functions

### `create_stability_analyzer(config)`

Factory function to create stability analyzer.

Parameters
----------
config : Dict[str, Any], optional
    Configuration parameters

Returns
-------
StabilityAnalyzer
    Configured stability analyzer

#### Source Code

```{literalinclude} ../../../src/analysis/performance/stability_analysis.py
:language: python
:pyobject: create_stability_analyzer
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Dict, List, Optional, Tuple, Any, Union`
- `import numpy as np`
- `from scipy import linalg, signal`
- `import warnings`
- `from dataclasses import dataclass`
- `from ..core.interfaces import PerformanceAnalyzer, AnalysisResult, AnalysisStatus, DataProtocol`
- `from ..core.data_structures import MetricResult, PerformanceMetrics`
