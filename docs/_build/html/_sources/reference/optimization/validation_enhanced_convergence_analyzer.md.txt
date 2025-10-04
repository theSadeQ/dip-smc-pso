# optimization.validation.enhanced_convergence_analyzer

**Source:** `src\optimization\validation\enhanced_convergence_analyzer.py`

## Module Overview

Enhanced PSO Convergence Criteria and Validation Algorithms.

This module provides advanced convergence analysis and validation algorithms
for PSO optimization in the controller factory integration context. Features
include multi-criteria convergence detection, statistical validation, and
real-time convergence monitoring.

Key Features:
- Multi-modal convergence detection
- Statistical significance testing
- Real-time convergence monitoring
- Adaptive convergence criteria
- Population diversity analysis
- Performance prediction algorithms

## Complete Source Code

```{literalinclude} ../../../src/optimization/validation/enhanced_convergence_analyzer.py
:language: python
:linenos:
```

---

## Classes

### `ConvergenceStatus`

**Inherits from:** `Enum`

Enhanced convergence status indicators.

#### Source Code

```{literalinclude} ../../../src/optimization/validation/enhanced_convergence_analyzer.py
:language: python
:pyobject: ConvergenceStatus
:linenos:
```

---

### `ConvergenceCriterion`

**Inherits from:** `Enum`

Types of convergence criteria.

#### Source Code

```{literalinclude} ../../../src/optimization/validation/enhanced_convergence_analyzer.py
:language: python
:pyobject: ConvergenceCriterion
:linenos:
```

---

### `ConvergenceMetrics`

Comprehensive convergence metrics.

#### Source Code

```{literalinclude} ../../../src/optimization/validation/enhanced_convergence_analyzer.py
:language: python
:pyobject: ConvergenceMetrics
:linenos:
```

---

### `ConvergenceCriteria`

Adaptive convergence criteria configuration.

#### Source Code

```{literalinclude} ../../../src/optimization/validation/enhanced_convergence_analyzer.py
:language: python
:pyobject: ConvergenceCriteria
:linenos:
```

---

### `EnhancedConvergenceAnalyzer`

Advanced PSO convergence analysis with multi-criteria validation.

Provides comprehensive convergence monitoring, statistical validation,
and performance prediction for PSO optimization in controller factory
integration scenarios.

#### Source Code

```{literalinclude} ../../../src/optimization/validation/enhanced_convergence_analyzer.py
:language: python
:pyobject: EnhancedConvergenceAnalyzer
:linenos:
```

#### Methods (17)

##### `__init__(self, criteria, controller_type)`

Initialize enhanced convergence analyzer.

[View full source →](#method-enhancedconvergenceanalyzer-__init__)

##### `_apply_controller_specific_tuning(self)`

Apply controller-specific convergence criteria tuning.

[View full source →](#method-enhancedconvergenceanalyzer-_apply_controller_specific_tuning)

##### `analyze_convergence(self, iteration, best_fitness, population_fitness, population_positions)`

Comprehensive convergence analysis for current PSO iteration.

[View full source →](#method-enhancedconvergenceanalyzer-analyze_convergence)

##### `check_convergence(self, metrics)`

Multi-criteria convergence check with detailed analysis.

[View full source →](#method-enhancedconvergenceanalyzer-check_convergence)

##### `_calculate_population_diversity(self, positions)`

Calculate population diversity using average pairwise distance.

[View full source →](#method-enhancedconvergenceanalyzer-_calculate_population_diversity)

##### `_calculate_convergence_velocity(self)`

Calculate convergence velocity using fitness improvement rate.

[View full source →](#method-enhancedconvergenceanalyzer-_calculate_convergence_velocity)

##### `_calculate_improvement_rate(self)`

Calculate relative improvement rate over recent iterations.

[View full source →](#method-enhancedconvergenceanalyzer-_calculate_improvement_rate)

##### `_calculate_stagnation_score(self)`

Calculate stagnation score based on recent fitness variations.

[View full source →](#method-enhancedconvergenceanalyzer-_calculate_stagnation_score)

##### `_calculate_diversity_loss_rate(self)`

Calculate rate of population diversity loss.

[View full source →](#method-enhancedconvergenceanalyzer-_calculate_diversity_loss_rate)

##### `_predict_remaining_iterations(self)`

Predict remaining iterations until convergence.

[View full source →](#method-enhancedconvergenceanalyzer-_predict_remaining_iterations)

##### `_estimate_convergence_probability(self)`

Estimate probability of successful convergence.

[View full source →](#method-enhancedconvergenceanalyzer-_estimate_convergence_probability)

##### `_calculate_statistical_confidence(self)`

Calculate statistical confidence in convergence assessment.

[View full source →](#method-enhancedconvergenceanalyzer-_calculate_statistical_confidence)

##### `_check_statistical_convergence(self)`

Check for statistical convergence using hypothesis testing.

[View full source →](#method-enhancedconvergenceanalyzer-_check_statistical_convergence)

##### `_detect_premature_convergence(self, metrics)`

Detect premature convergence conditions.

[View full source →](#method-enhancedconvergenceanalyzer-_detect_premature_convergence)

##### `_update_convergence_status(self, metrics)`

Update internal convergence status based on metrics.

[View full source →](#method-enhancedconvergenceanalyzer-_update_convergence_status)

##### `get_convergence_diagnostics(self)`

Get comprehensive convergence diagnostics.

[View full source →](#method-enhancedconvergenceanalyzer-get_convergence_diagnostics)

##### `export_convergence_analysis(self, output_path)`

Export detailed convergence analysis.

[View full source →](#method-enhancedconvergenceanalyzer-export_convergence_analysis)

---

### `PSOConvergenceValidator`

Validation framework for PSO convergence algorithms.

Tests and validates convergence detection accuracy across different
optimization scenarios and controller types.

#### Source Code

```{literalinclude} ../../../src/optimization/validation/enhanced_convergence_analyzer.py
:language: python
:pyobject: PSOConvergenceValidator
:linenos:
```

#### Methods (3)

##### `__init__(self)`

Initialize PSO convergence validator.

[View full source →](#method-psoconvergencevalidator-__init__)

##### `validate_convergence_detection(self, controller_type, test_scenarios)`

Validate convergence detection accuracy for controller type.

[View full source →](#method-psoconvergencevalidator-validate_convergence_detection)

##### `_run_convergence_test_scenario(self, controller_type, scenario)`

Run a single convergence detection test scenario.

[View full source →](#method-psoconvergencevalidator-_run_convergence_test_scenario)

---

## Functions

### `run_enhanced_convergence_validation()`

Run comprehensive PSO convergence validation.

#### Source Code

```{literalinclude} ../../../src/optimization/validation/enhanced_convergence_analyzer.py
:language: python
:pyobject: run_enhanced_convergence_validation
:linenos:
```

---

## Dependencies

This module imports:

- `import numpy as np`
- `import logging`
- `from typing import Dict, List, Tuple, Any, Optional, Callable, Union`
- `from dataclasses import dataclass, field`
- `from enum import Enum`
- `import time`
- `from scipy import stats`
- `from scipy.signal import savgol_filter`
- `import warnings`
- `from src.controllers.factory import SMCType`

*... and 3 more*
