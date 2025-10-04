# analysis.core.metrics

**Source:** `src\analysis\core\metrics.py`

## Module Overview

Core metric computation framework.

This module provides the foundation for computing various performance
metrics from simulation data, with emphasis on control engineering
applications and statistical rigor.

## Complete Source Code

```{literalinclude} ../../../src/analysis/core/metrics.py
:language: python
:linenos:
```

---

## Classes

### `BaseMetricCalculator`

**Inherits from:** `MetricCalculator`

Base implementation of metric calculator with common functionality.

#### Source Code

```{literalinclude} ../../../src/analysis/core/metrics.py
:language: python
:pyobject: BaseMetricCalculator
:linenos:
```

#### Methods (4)

##### `__init__(self, validate_inputs)`

Initialize base metric calculator.

[View full source →](#method-basemetriccalculator-__init__)

##### `compute(self, data)`

Compute metrics from simulation data.

[View full source →](#method-basemetriccalculator-compute)

##### `_compute_metric(self, metric_name, data)`

Compute a specific metric. Override in subclasses.

[View full source →](#method-basemetriccalculator-_compute_metric)

##### `supported_metrics(self)`

List of supported metrics.

[View full source →](#method-basemetriccalculator-supported_metrics)

---

### `ControlPerformanceMetrics`

**Inherits from:** `BaseMetricCalculator`

Calculator for control performance metrics.

#### Source Code

```{literalinclude} ../../../src/analysis/core/metrics.py
:language: python
:pyobject: ControlPerformanceMetrics
:linenos:
```

#### Methods (10)

##### `__init__(self, reference_tolerance)`

Initialize control performance metrics calculator.

[View full source →](#method-controlperformancemetrics-__init__)

##### `supported_metrics(self)`

List of supported control performance metrics.

[View full source →](#method-controlperformancemetrics-supported_metrics)

##### `_compute_metric(self, metric_name, data)`

Compute specific control performance metric.

[View full source →](#method-controlperformancemetrics-_compute_metric)

##### `_compute_tracking_error_metric(self, metric_name, data, reference, output_indices)`

Compute tracking error metrics.

[View full source →](#method-controlperformancemetrics-_compute_tracking_error_metric)

##### `_compute_transient_metric(self, metric_name, data, reference, output_indices)`

Compute transient response metrics.

[View full source →](#method-controlperformancemetrics-_compute_transient_metric)

##### `_compute_control_metric(self, metric_name, data)`

Compute control effort metrics.

[View full source →](#method-controlperformancemetrics-_compute_control_metric)

##### `_compute_settling_time(self, times, output)`

Compute settling time using percentage criteria.

[View full source →](#method-controlperformancemetrics-_compute_settling_time)

##### `_compute_overshoot(self, output)`

Compute maximum overshoot percentage.

[View full source →](#method-controlperformancemetrics-_compute_overshoot)

##### `_compute_rise_time(self, times, output)`

Compute rise time (10% to 90% of final value).

[View full source →](#method-controlperformancemetrics-_compute_rise_time)

##### `_compute_steady_state_error(self, output, reference)`

Compute steady-state error.

[View full source →](#method-controlperformancemetrics-_compute_steady_state_error)

---

### `StabilityMetrics`

**Inherits from:** `BaseMetricCalculator`

Calculator for stability-related metrics.

#### Source Code

```{literalinclude} ../../../src/analysis/core/metrics.py
:language: python
:pyobject: StabilityMetrics
:linenos:
```

#### Methods (4)

##### `supported_metrics(self)`

List of supported stability metrics.

[View full source →](#method-stabilitymetrics-supported_metrics)

##### `_compute_metric(self, metric_name, data)`

Compute specific stability metric.

[View full source →](#method-stabilitymetrics-_compute_metric)

##### `_compute_lyapunov_exponent(self, data)`

Estimate largest Lyapunov exponent from time series.

[View full source →](#method-stabilitymetrics-_compute_lyapunov_exponent)

##### `_compute_bounded_states(self, data, bounds)`

Compute fraction of time states remain within bounds.

[View full source →](#method-stabilitymetrics-_compute_bounded_states)

---

### `RobustnessMetrics`

**Inherits from:** `BaseMetricCalculator`

Calculator for robustness metrics.

#### Source Code

```{literalinclude} ../../../src/analysis/core/metrics.py
:language: python
:pyobject: RobustnessMetrics
:linenos:
```

#### Methods (2)

##### `supported_metrics(self)`

List of supported robustness metrics.

[View full source →](#method-robustnessmetrics-supported_metrics)

##### `_compute_metric(self, metric_name, data)`

Compute specific robustness metric.

[View full source →](#method-robustnessmetrics-_compute_metric)

---

## Functions

### `create_comprehensive_metrics(data, reference, include_stability, include_robustness)`

Create comprehensive performance metrics from simulation data.

Parameters
----------
data : DataProtocol
    Simulation data
reference : np.ndarray, optional
    Reference trajectory for tracking metrics
include_stability : bool, optional
    Whether to include stability metrics
include_robustness : bool, optional
    Whether to include robustness metrics
**kwargs
    Additional parameters for metric calculation

Returns
-------
PerformanceMetrics
    Comprehensive collection of performance metrics

#### Source Code

```{literalinclude} ../../../src/analysis/core/metrics.py
:language: python
:pyobject: create_comprehensive_metrics
:linenos:
```

---

### `_get_metric_unit(metric_name)`

Get appropriate unit for a metric.

#### Source Code

```{literalinclude} ../../../src/analysis/core/metrics.py
:language: python
:pyobject: _get_metric_unit
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Dict, List, Optional, Tuple, Any`
- `import numpy as np`
- `from scipy import signal, integrate`
- `import warnings`
- `from .interfaces import MetricCalculator, DataProtocol`
- `from .data_structures import MetricResult, PerformanceMetrics`
