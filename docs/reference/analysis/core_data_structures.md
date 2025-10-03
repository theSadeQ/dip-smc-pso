# analysis.core.data_structures

**Source:** `src\analysis\core\data_structures.py`

## Module Overview

Data structures for analysis framework.

This module provides standardized data structures for representing
simulation data, analysis results, and configuration parameters.

## Complete Source Code

```{literalinclude} ../../../src/analysis/core/data_structures.py
:language: python
:linenos:
```

---

## Classes

### `SimulationData`

Standard container for simulation data.

#### Source Code

```{literalinclude} ../../../src/analysis/core/data_structures.py
:language: python
:pyobject: SimulationData
:linenos:
```

#### Methods (7)

##### `__post_init__(self)`

Validate data consistency after initialization.

[View full source →](#method-simulationdata-__post_init__)

##### `_validate_dimensions(self)`

Validate dimensional consistency of arrays.

[View full source →](#method-simulationdata-_validate_dimensions)

##### `get_time_range(self)`

Get time range of the data.

[View full source →](#method-simulationdata-get_time_range)

##### `get_sampling_rate(self)`

Get average sampling rate.

[View full source →](#method-simulationdata-get_sampling_rate)

##### `get_duration(self)`

Get total simulation duration.

[View full source →](#method-simulationdata-get_duration)

##### `extract_slice(self, start_time, end_time)`

Extract a time slice of the data.

[View full source →](#method-simulationdata-extract_slice)

##### `downsample(self, factor)`

Downsample the data by the given factor.

[View full source →](#method-simulationdata-downsample)

---

### `MetricResult`

Container for individual metric results.

#### Source Code

```{literalinclude} ../../../src/analysis/core/data_structures.py
:language: python
:pyobject: MetricResult
:linenos:
```

#### Methods (1)

##### `__str__(self)`

String representation of the metric.

[View full source →](#method-metricresult-__str__)

---

### `PerformanceMetrics`

Container for performance metrics.

#### Source Code

```{literalinclude} ../../../src/analysis/core/data_structures.py
:language: python
:pyobject: PerformanceMetrics
:linenos:
```

#### Methods (5)

##### `add_metric(self, metric)`

Add a metric to the collection.

[View full source →](#method-performancemetrics-add_metric)

##### `get_metric(self, name)`

Get a metric by name.

[View full source →](#method-performancemetrics-get_metric)

##### `get_metric_value(self, name)`

Get a metric value by name.

[View full source →](#method-performancemetrics-get_metric_value)

##### `to_dict(self)`

Convert metrics to dictionary for compatibility.

[View full source →](#method-performancemetrics-to_dict)

##### `summary_statistics(self)`

Compute summary statistics of all metrics.

[View full source →](#method-performancemetrics-summary_statistics)

---

### `FaultDetectionResult`

Container for fault detection results.

#### Source Code

```{literalinclude} ../../../src/analysis/core/data_structures.py
:language: python
:pyobject: FaultDetectionResult
:linenos:
```

#### Methods (2)

##### `is_fault_detected(self)`

Check if a fault was detected.

[View full source →](#method-faultdetectionresult-is_fault_detected)

##### `has_warnings(self)`

Check if there are warnings.

[View full source →](#method-faultdetectionresult-has_warnings)

---

### `StatisticalTestResult`

Container for statistical test results.

#### Source Code

```{literalinclude} ../../../src/analysis/core/data_structures.py
:language: python
:pyobject: StatisticalTestResult
:linenos:
```

#### Methods (2)

##### `is_significant(self, alpha)`

Check if result is statistically significant.

[View full source →](#method-statisticaltestresult-is_significant)

##### `__str__(self)`

String representation of test result.

[View full source →](#method-statisticaltestresult-__str__)

---

### `ConfidenceInterval`

Container for confidence intervals.

#### Source Code

```{literalinclude} ../../../src/analysis/core/data_structures.py
:language: python
:pyobject: ConfidenceInterval
:linenos:
```

#### Methods (4)

##### `width(self)`

Width of the confidence interval.

[View full source →](#method-confidenceinterval-width)

##### `center(self)`

Center of the confidence interval.

[View full source →](#method-confidenceinterval-center)

##### `contains(self, value)`

Check if value is within the confidence interval.

[View full source →](#method-confidenceinterval-contains)

##### `__str__(self)`

String representation of confidence interval.

[View full source →](#method-confidenceinterval-__str__)

---

### `ComparisonResult`

Container for comparison analysis results.

#### Source Code

```{literalinclude} ../../../src/analysis/core/data_structures.py
:language: python
:pyobject: ComparisonResult
:linenos:
```

#### Methods (1)

##### `get_winner(self, metric, lower_is_better)`

Determine the winning method for a specific metric.

[View full source →](#method-comparisonresult-get_winner)

---

### `AnalysisConfiguration`

Configuration for analysis operations.

#### Source Code

```{literalinclude} ../../../src/analysis/core/data_structures.py
:language: python
:pyobject: AnalysisConfiguration
:linenos:
```

#### Methods (2)

##### `__post_init__(self)`

Set default configurations if not provided.

[View full source →](#method-analysisconfiguration-__post_init__)

##### `validate(self)`

Validate configuration parameters.

[View full source →](#method-analysisconfiguration-validate)

---

## Functions

### `create_simulation_data_from_arrays(times, states, controls)`

Factory function for creating SimulationData.

#### Source Code

```{literalinclude} ../../../src/analysis/core/data_structures.py
:language: python
:pyobject: create_simulation_data_from_arrays
:linenos:
```

---

### `create_analysis_result(status, message, data)`

Factory function for creating AnalysisResult.

#### Source Code

```{literalinclude} ../../../src/analysis/core/data_structures.py
:language: python
:pyobject: create_analysis_result
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from dataclasses import dataclass, field`
- `from typing import Any, Dict, List, Optional, Tuple, Union`
- `import numpy as np`
- `from datetime import datetime`
- `from .interfaces import DataProtocol, AnalysisResult, AnalysisStatus`
