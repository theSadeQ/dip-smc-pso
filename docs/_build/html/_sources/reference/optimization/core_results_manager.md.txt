# optimization.core.results_manager

**Source:** `src\optimization\core\results_manager.py`

## Module Overview

PSO Optimization Results Management and Serialization.

This module provides comprehensive management of PSO optimization results including
serialization, loading, analysis, and comparison capabilities. It ensures reproducible
optimization workflows and enables advanced result analysis.

Features:
- Comprehensive result serialization (JSON, HDF5, NPZ)
- Metadata tracking and provenance
- Result comparison and benchmarking
- Statistical analysis of optimization runs
- Convergence analysis and visualization
- Result validation and integrity checking

References:
- IEEE Standard for Software Configuration Management Plans
- Best practices for scientific computing reproducibility

## Complete Source Code

```{literalinclude} ../../../src/optimization/core/results_manager.py
:language: python
:linenos:
```

---

## Classes

### `OptimizationMetadata`

Comprehensive metadata for optimization results.

#### Source Code

```{literalinclude} ../../../src/optimization/core/results_manager.py
:language: python
:pyobject: OptimizationMetadata
:linenos:
```

---

### `OptimizationResults`

Complete optimization results structure.

#### Source Code

```{literalinclude} ../../../src/optimization/core/results_manager.py
:language: python
:pyobject: OptimizationResults
:linenos:
```

---

### `OptimizationResultsManager`

Advanced management system for PSO optimization results.

This class provides comprehensive functionality for storing, loading, analyzing,
and comparing optimization results with full provenance tracking.

#### Source Code

```{literalinclude} ../../../src/optimization/core/results_manager.py
:language: python
:pyobject: OptimizationResultsManager
:linenos:
```

#### Methods (16)

##### `__init__(self, results_directory)`

[View full source →](#method-optimizationresultsmanager-__init__)

##### `save_results(self, results, run_id, format)`

Save optimization results with comprehensive metadata.

[View full source →](#method-optimizationresultsmanager-save_results)

##### `_save_json(self, results, run_id)`

Save results in JSON format.

[View full source →](#method-optimizationresultsmanager-_save_json)

##### `_save_hdf5(self, results, run_id)`

Save results in HDF5 format for large datasets.

[View full source →](#method-optimizationresultsmanager-_save_hdf5)

##### `_save_npz(self, results, run_id)`

Save results in NumPy NPZ format.

[View full source →](#method-optimizationresultsmanager-_save_npz)

##### `load_results(self, filepath)`

Load optimization results from file.

[View full source →](#method-optimizationresultsmanager-load_results)

##### `_load_json(self, filepath)`

Load results from JSON file.

[View full source →](#method-optimizationresultsmanager-_load_json)

##### `_load_npz(self, filepath)`

Load results from NPZ file.

[View full source →](#method-optimizationresultsmanager-_load_npz)

##### `compare_results(self, result_paths, metrics)`

Compare multiple optimization results.

[View full source →](#method-optimizationresultsmanager-compare_results)

##### `_calculate_statistics(self, results)`

Calculate comprehensive statistics for optimization results.

[View full source →](#method-optimizationresultsmanager-_calculate_statistics)

##### `_detect_stagnation_periods(self, convergence, threshold)`

Detect periods of stagnation in convergence history.

[View full source →](#method-optimizationresultsmanager-_detect_stagnation_periods)

##### `_calculate_clustering_coefficient(self, population)`

Calculate clustering coefficient of final population.

[View full source →](#method-optimizationresultsmanager-_calculate_clustering_coefficient)

##### `_perform_statistical_tests(self, results)`

Perform statistical significance tests on results.

[View full source →](#method-optimizationresultsmanager-_perform_statistical_tests)

##### `_generate_comparison_recommendations(self, results, comparison)`

Generate recommendations based on comparison analysis.

[View full source →](#method-optimizationresultsmanager-_generate_comparison_recommendations)

##### `_make_json_serializable(self, obj)`

Convert object to JSON-serializable format.

[View full source →](#method-optimizationresultsmanager-_make_json_serializable)

##### `generate_results_summary(self, run_id_pattern)`

Generate summary of all results matching pattern.

[View full source →](#method-optimizationresultsmanager-generate_results_summary)

---

## Functions

### `create_optimization_metadata(controller_type, config, seed)`

Create optimization metadata from configuration.

Parameters
----------
controller_type : str
    Type of controller being optimized
config : Dict[str, Any]
    Configuration dictionary
seed : int, optional
    Random seed used

Returns
-------
OptimizationMetadata
    Complete metadata object

#### Source Code

```{literalinclude} ../../../src/optimization/core/results_manager.py
:language: python
:pyobject: create_optimization_metadata
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import json`
- `import logging`
- `import numpy as np`
- `import hashlib`
- `from datetime import datetime`
- `from pathlib import Path`
- `from typing import Any, Dict, List, Optional, Tuple, Union`
- `from dataclasses import dataclass, asdict`
- `import warnings`

*... and 1 more*
