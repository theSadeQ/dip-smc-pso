# analysis.validation.metrics

**Source:** `src\analysis\validation\metrics.py`

## Module Overview

Statistical and validation metrics for analysis systems.

This module provides comprehensive metrics computation for validating
control system performance, statistical analysis, and benchmarking.

## Complete Source Code

```{literalinclude} ../../../src/analysis/validation/metrics.py
:language: python
:linenos:
```

---

## Functions

### `compute_basic_metrics(data)`

Compute basic statistical metrics for data analysis.

Args:
    data: Input data array

Returns:
    Dictionary containing basic statistical metrics

#### Source Code

```{literalinclude} ../../../src/analysis/validation/metrics.py
:language: python
:pyobject: compute_basic_metrics
:linenos:
```

---

### `compute_performance_metrics(reference, actual)`

Compute performance metrics comparing actual vs reference data.

Args:
    reference: Reference/target data
    actual: Actual measured data

Returns:
    Dictionary containing performance metrics

#### Source Code

```{literalinclude} ../../../src/analysis/validation/metrics.py
:language: python
:pyobject: compute_performance_metrics
:linenos:
```

---

### `compute_control_metrics(control_signals, time_vector)`

Compute control-specific performance metrics.

Args:
    control_signals: Control input signals over time
    time_vector: Optional time vector for time-based metrics

Returns:
    Dictionary containing control metrics

#### Source Code

```{literalinclude} ../../../src/analysis/validation/metrics.py
:language: python
:pyobject: compute_control_metrics
:linenos:
```

---

### `compute_stability_metrics(states, reference_state)`

Compute stability-related metrics for state trajectories.

Args:
    states: State trajectory matrix (time x state_dim)
    reference_state: Optional reference state for deviation metrics

Returns:
    Dictionary containing stability metrics

#### Source Code

```{literalinclude} ../../../src/analysis/validation/metrics.py
:language: python
:pyobject: compute_stability_metrics
:linenos:
```

---

### `compute_frequency_metrics(signal, sampling_rate, frequency_bands)`

Compute frequency domain metrics for signal analysis.

Args:
    signal: Input signal
    sampling_rate: Sampling rate in Hz
    frequency_bands: Optional list of (low, high) frequency bands

Returns:
    Dictionary containing frequency domain metrics

#### Source Code

```{literalinclude} ../../../src/analysis/validation/metrics.py
:language: python
:pyobject: compute_frequency_metrics
:linenos:
```

---

### `compute_statistical_significance(data1, data2, test_type)`

Compute statistical significance between two data sets.

Args:
    data1: First data set
    data2: Second data set
    test_type: Type of statistical test ('ttest', 'mannwhitney', 'ks')

Returns:
    Dictionary containing test statistics and p-value

#### Source Code

```{literalinclude} ../../../src/analysis/validation/metrics.py
:language: python
:pyobject: compute_statistical_significance
:linenos:
```

---

### `compute_robustness_metrics(nominal_performance, perturbed_performances, metric_names)`

Compute robustness metrics comparing nominal vs perturbed performance.

Args:
    nominal_performance: Performance metrics for nominal conditions
    perturbed_performances: List of performance metrics under perturbations
    metric_names: Optional list of metric names to analyze

Returns:
    Dictionary of robustness metrics for each performance metric

#### Source Code

```{literalinclude} ../../../src/analysis/validation/metrics.py
:language: python
:pyobject: compute_robustness_metrics
:linenos:
```

---

### `compute_comprehensive_metrics(states, controls, time_vector, reference_states, reference_controls)`

Compute comprehensive metrics for control system analysis.

Args:
    states: State trajectory matrix
    controls: Control signal vector
    time_vector: Time vector
    reference_states: Optional reference state trajectory
    reference_controls: Optional reference control signals

Returns:
    Dictionary containing comprehensive metrics

#### Source Code

```{literalinclude} ../../../src/analysis/validation/metrics.py
:language: python
:pyobject: compute_comprehensive_metrics
:linenos:
```

---

## Dependencies

This module imports:

- `from typing import Dict, List, Tuple, Any, Optional, Union`
- `import numpy as np`
- `from scipy import stats`
- `import warnings`
