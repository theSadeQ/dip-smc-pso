# analysis.__init__

**Source:** `src\analysis\__init__.py`

## Module Overview

Professional analysis framework for control system evaluation and validation.

This module provides a comprehensive analysis framework including:
- Core analysis interfaces and data structures
- Performance metrics and evaluation
- Fault detection and isolation
- Statistical validation and testing
- Monte Carlo analysis
- Cross-validation methods
- Visualization and reporting

The framework follows control engineering best practices and provides both
legacy compatibility and modern enhanced capabilities.

## Complete Source Code

```{literalinclude} ../../../src/analysis/__init__.py
:language: python
:linenos:
```

---

## Functions

### `create_performance_analyzer(analyzer_type)`

Create performance analyzer instance.

Parameters
----------
analyzer_type : str
    Type of analyzer ('advanced', 'stability', 'robustness')
**kwargs
    Additional configuration parameters

Returns
-------
PerformanceAnalyzer
    Configured performance analyzer

#### Source Code

```{literalinclude} ../../../src/analysis/__init__.py
:language: python
:pyobject: create_performance_analyzer
:linenos:
```

---

### `create_fault_detector(detector_type)`

Create fault detector instance.

Parameters
----------
detector_type : str
    Type of detector ('enhanced', 'legacy')
**kwargs
    Additional configuration parameters

Returns
-------
FaultDetector
    Configured fault detector

#### Source Code

```{literalinclude} ../../../src/analysis/__init__.py
:language: python
:pyobject: create_fault_detector
:linenos:
```

---

### `create_statistical_validator()`

Create statistical validator instance.

#### Source Code

```{literalinclude} ../../../src/analysis/__init__.py
:language: python
:pyobject: create_statistical_validator
:linenos:
```

---

### `create_monte_carlo_analyzer()`

Create Monte Carlo analyzer instance.

#### Source Code

```{literalinclude} ../../../src/analysis/__init__.py
:language: python
:pyobject: create_monte_carlo_analyzer
:linenos:
```

---

### `create_visualization_suite()`

Create complete visualization suite.

#### Source Code

```{literalinclude} ../../../src/analysis/__init__.py
:language: python
:pyobject: create_visualization_suite
:linenos:
```

---

## Dependencies

This module imports:

- `from .core.interfaces import AnalysisResult, AnalysisStatus, DataProtocol, MetricCalculator, PerformanceAnalyzer, FaultDetector, StatisticalValidator`
- `from .core.data_structures import SimulationData, MetricResult, PerformanceMetrics, FaultDetectionResult, StatisticalTestResult, ConfidenceInterval`
- `from .core.metrics import BaseMetricCalculator, ControlPerformanceMetrics, StabilityMetrics`
- `from .performance.control_metrics import AdvancedControlMetrics, compute_ise, compute_itae, compute_rms_control_effort`
- `from .performance.stability_analysis import StabilityAnalyzer`
- `from .performance.robustness import RobustnessAnalyzer`
- `from .fault_detection.fdi_system import EnhancedFaultDetector, FaultDetectionConfig, FaultType, DetectionMethod, create_enhanced_fault_detector, FDIsystem, FaultDetectionInterface, DynamicsProtocol`
- `from .fault_detection.residual_generators import ResidualGeneratorFactory, ObserverBasedGenerator, KalmanFilterGenerator, ParitySpaceGenerator`
- `from .fault_detection.threshold_adapters import ThresholdAdapterFactory, StatisticalThresholdAdapter, EWMAThresholdAdapter, AdaptiveThresholdManager`
- `from .validation.statistical_tests import StatisticalTestSuite`

*... and 7 more*
