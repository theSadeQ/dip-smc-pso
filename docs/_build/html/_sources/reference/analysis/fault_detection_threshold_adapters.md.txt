# analysis.fault_detection.threshold_adapters

**Source:** `src\analysis\fault_detection\threshold_adapters.py`

## Module Overview

Adaptive threshold methods for fault detection.

This module provides various adaptive thresholding techniques to improve
fault detection performance under varying operating conditions and
system uncertainties.

## Complete Source Code

```{literalinclude} ../../../src/analysis/fault_detection/threshold_adapters.py
:language: python
:linenos:
```

---

## Classes

### `ThresholdAdapterConfig`

Configuration for threshold adapters.

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/threshold_adapters.py
:language: python
:pyobject: ThresholdAdapterConfig
:linenos:
```

---

### `ThresholdAdapter`

**Inherits from:** `ABC`

Abstract base class for threshold adapters.

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/threshold_adapters.py
:language: python
:pyobject: ThresholdAdapter
:linenos:
```

#### Methods (3)

##### `update(self, residual, timestamp)`

Update threshold based on new residual value.

[View full source →](#method-thresholdadapter-update)

##### `reset(self)`

Reset adapter state.

[View full source →](#method-thresholdadapter-reset)

##### `current_threshold(self)`

Current threshold value.

[View full source →](#method-thresholdadapter-current_threshold)

---

### `StatisticalThresholdAdapter`

**Inherits from:** `ThresholdAdapter`

Statistical adaptive threshold based on residual statistics.

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/threshold_adapters.py
:language: python
:pyobject: StatisticalThresholdAdapter
:linenos:
```

#### Methods (10)

##### `__init__(self, config)`

Initialize statistical threshold adapter.

[View full source →](#method-statisticalthresholdadapter-__init__)

##### `update(self, residual, timestamp)`

Update threshold using statistical methods.

[View full source →](#method-statisticalthresholdadapter-update)

##### `_compute_statistical_threshold(self)`

Compute threshold using statistical methods.

[View full source →](#method-statisticalthresholdadapter-_compute_statistical_threshold)

##### `_reject_outliers(self, data)`

Reject outliers using IQR or Z-score method.

[View full source →](#method-statisticalthresholdadapter-_reject_outliers)

##### `_robust_parameter_estimation(self, data)`

Robust estimation of location and scale parameters.

[View full source →](#method-statisticalthresholdadapter-_robust_parameter_estimation)

##### `_gaussian_threshold(self, location, scale)`

Compute threshold assuming Gaussian distribution.

[View full source →](#method-statisticalthresholdadapter-_gaussian_threshold)

##### `_chi_squared_threshold(self, data)`

Compute threshold using chi-squared distribution.

[View full source →](#method-statisticalthresholdadapter-_chi_squared_threshold)

##### `_t_distribution_threshold(self, data)`

Compute threshold using t-distribution.

[View full source →](#method-statisticalthresholdadapter-_t_distribution_threshold)

##### `reset(self)`

Reset adapter state.

[View full source →](#method-statisticalthresholdadapter-reset)

##### `current_threshold(self)`

Current threshold value.

[View full source →](#method-statisticalthresholdadapter-current_threshold)

---

### `EWMAThresholdAdapter`

**Inherits from:** `ThresholdAdapter`

Exponentially Weighted Moving Average threshold adapter.

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/threshold_adapters.py
:language: python
:pyobject: EWMAThresholdAdapter
:linenos:
```

#### Methods (4)

##### `__init__(self, config)`

Initialize EWMA threshold adapter.

[View full source →](#method-ewmathresholdadapter-__init__)

##### `update(self, residual, timestamp)`

Update threshold using EWMA.

[View full source →](#method-ewmathresholdadapter-update)

##### `reset(self)`

Reset adapter state.

[View full source →](#method-ewmathresholdadapter-reset)

##### `current_threshold(self)`

Current threshold value.

[View full source →](#method-ewmathresholdadapter-current_threshold)

---

### `ChangeDetectionThresholdAdapter`

**Inherits from:** `ThresholdAdapter`

Threshold adapter with change detection capability.

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/threshold_adapters.py
:language: python
:pyobject: ChangeDetectionThresholdAdapter
:linenos:
```

#### Methods (7)

##### `__init__(self, config, base_adapter)`

Initialize change detection adapter.

[View full source →](#method-changedetectionthresholdadapter-__init__)

##### `update(self, residual, timestamp)`

Update threshold with change detection.

[View full source →](#method-changedetectionthresholdadapter-update)

##### `_detect_change(self)`

Detect change points in residual sequence.

[View full source →](#method-changedetectionthresholdadapter-_detect_change)

##### `_cusum_change_detection(self, data)`

CUSUM-based change detection.

[View full source →](#method-changedetectionthresholdadapter-_cusum_change_detection)

##### `_handle_change_detection(self)`

Handle detected change point.

[View full source →](#method-changedetectionthresholdadapter-_handle_change_detection)

##### `reset(self)`

Reset adapter state.

[View full source →](#method-changedetectionthresholdadapter-reset)

##### `current_threshold(self)`

Current threshold value.

[View full source →](#method-changedetectionthresholdadapter-current_threshold)

---

### `MultivariatethresholdAdapter`

**Inherits from:** `ThresholdAdapter`

Multivariate threshold adapter for vector residuals.

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/threshold_adapters.py
:language: python
:pyobject: MultivariatethresholdAdapter
:linenos:
```

#### Methods (5)

##### `__init__(self, config, dimension)`

Initialize multivariate threshold adapter.

[View full source →](#method-multivariatethresholdadapter-__init__)

##### `update(self, residual, timestamp)`

Update threshold for vector residual.

[View full source →](#method-multivariatethresholdadapter-update)

##### `_compute_multivariate_threshold(self)`

Compute threshold for multivariate residuals.

[View full source →](#method-multivariatethresholdadapter-_compute_multivariate_threshold)

##### `reset(self)`

Reset adapter state.

[View full source →](#method-multivariatethresholdadapter-reset)

##### `current_threshold(self)`

Current threshold value.

[View full source →](#method-multivariatethresholdadapter-current_threshold)

---

### `AdaptiveThresholdManager`

Manager for multiple threshold adapters with different methods.

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/threshold_adapters.py
:language: python
:pyobject: AdaptiveThresholdManager
:linenos:
```

#### Methods (8)

##### `__init__(self, methods, config)`

Initialize adaptive threshold manager.

[View full source →](#method-adaptivethresholdmanager-__init__)

##### `_create_adapter(self, method)`

Create adapter for specified method.

[View full source →](#method-adaptivethresholdmanager-_create_adapter)

##### `update(self, residual, timestamp)`

Update all adapters and return thresholds.

[View full source →](#method-adaptivethresholdmanager-update)

##### `get_consensus_threshold(self, method)`

Get consensus threshold from all adapters.

[View full source →](#method-adaptivethresholdmanager-get_consensus_threshold)

##### `get_threshold_statistics(self)`

Get statistics about current thresholds.

[View full source →](#method-adaptivethresholdmanager-get_threshold_statistics)

##### `reset(self)`

Reset all adapters.

[View full source →](#method-adaptivethresholdmanager-reset)

##### `update(self, residual, timestamp)`

Update and return consensus threshold.

[View full source →](#method-adaptivethresholdmanager-update)

##### `current_threshold(self)`

Current consensus threshold.

[View full source →](#method-adaptivethresholdmanager-current_threshold)

---

### `ThresholdAdapterFactory`

Factory class for creating threshold adapters.

This class provides a unified interface for creating different types of
threshold adapters used in fault detection systems.

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/threshold_adapters.py
:language: python
:pyobject: ThresholdAdapterFactory
:linenos:
```

#### Methods (5)

##### `create_adapter(method, config)`

Create a threshold adapter of the specified type.

[View full source →](#method-thresholdadapterfactory-create_adapter)

##### `get_available_methods()`

Get list of available threshold adaptation methods.

[View full source →](#method-thresholdadapterfactory-get_available_methods)

##### `create_manager(methods, config)`

Create an adaptive threshold manager with multiple methods.

[View full source →](#method-thresholdadapterfactory-create_manager)

##### `create_default_statistical(cls)`

Create statistical threshold adapter with default configuration.

[View full source →](#method-thresholdadapterfactory-create_default_statistical)

##### `create_default_ewma(cls, alpha)`

Create EWMA threshold adapter with default configuration.

[View full source →](#method-thresholdadapterfactory-create_default_ewma)

---

## Functions

### `create_threshold_adapter(method, config)`

Factory function to create threshold adapters.

Parameters
----------
method : str
    Type of adapter ('statistical', 'ewma', 'change_detection', 'multivariate')
config : ThresholdAdapterConfig, optional
    Configuration parameters
**kwargs
    Additional method-specific parameters

Returns
-------
ThresholdAdapter
    Configured threshold adapter

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/threshold_adapters.py
:language: python
:pyobject: create_threshold_adapter
:linenos:
```

---

### `create_adaptive_threshold_manager(methods, config)`

Factory function to create adaptive threshold manager.

Parameters
----------
methods : List[str]
    List of adaptation methods to use
config : ThresholdAdapterConfig, optional
    Configuration parameters

Returns
-------
AdaptiveThresholdManager
    Configured threshold manager

#### Source Code

```{literalinclude} ../../../src/analysis/fault_detection/threshold_adapters.py
:language: python
:pyobject: create_adaptive_threshold_manager
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Dict, List, Optional, Tuple, Any, Callable`
- `import numpy as np`
- `from scipy import stats, signal`
- `import warnings`
- `from dataclasses import dataclass, field`
- `from abc import ABC, abstractmethod`
- `from collections import deque`
- `from ..core.data_structures import ConfidenceInterval`
