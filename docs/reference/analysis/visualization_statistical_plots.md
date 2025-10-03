# analysis.visualization.statistical_plots

**Source:** `src\analysis\visualization\statistical_plots.py`

## Module Overview

Statistical visualization module for control system analysis.

This module provides specialized plotting capabilities for statistical analysis
of control system data, including distribution analysis, hypothesis test results,
and Monte Carlo simulation visualizations.

## Complete Source Code

```{literalinclude} ../../../src/analysis/visualization/statistical_plots.py
:language: python
:linenos:
```

---

## Classes

### `StatisticalPlotter`

Advanced statistical plotting for control system analysis.

#### Source Code

```{literalinclude} ../../../src/analysis/visualization/statistical_plots.py
:language: python
:pyobject: StatisticalPlotter
:linenos:
```

#### Methods (7)

##### `__init__(self, style, figsize)`

Initialize statistical plotter with scientific styling.

[View full source →](#method-statisticalplotter-__init__)

##### `_setup_style(self)`

Configure matplotlib style for scientific plots.

[View full source →](#method-statisticalplotter-_setup_style)

##### `plot_distribution_analysis(self, data, title, theoretical_dist, save_path)`

Create comprehensive distribution analysis plot.

[View full source →](#method-statisticalplotter-plot_distribution_analysis)

##### `plot_hypothesis_test_results(self, test_results, title, save_path)`

Visualize hypothesis test results.

[View full source →](#method-statisticalplotter-plot_hypothesis_test_results)

##### `plot_monte_carlo_results(self, simulation_results, confidence_levels, title, save_path)`

Visualize Monte Carlo simulation results.

[View full source →](#method-statisticalplotter-plot_monte_carlo_results)

##### `plot_correlation_matrix(self, data, labels, method, title, save_path)`

Create correlation matrix heatmap.

[View full source →](#method-statisticalplotter-plot_correlation_matrix)

##### `plot_convergence_analysis(self, convergence_data, title, save_path)`

Plot convergence behavior of iterative algorithms.

[View full source →](#method-statisticalplotter-plot_convergence_analysis)

---

## Dependencies

This module imports:

- `import matplotlib.pyplot as plt`
- `import matplotlib.patches as patches`
- `import numpy as np`
- `import pandas as pd`
- `from scipy import stats`
- `from typing import Dict, List, Optional, Tuple, Any, Union`
- `import warnings`
- `from ..core.interfaces import DataProtocol`
- `from ..core.data_structures import MetricResult`
