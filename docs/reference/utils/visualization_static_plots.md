# utils.visualization.static_plots

**Source:** `src\utils\visualization\static_plots.py`

## Module Overview

Static plotting utilities for control system analysis.

Provides comprehensive plotting functions for control system performance,
phase portraits, time series analysis, and system identification.

## Complete Source Code

```{literalinclude} ../../../src/utils/visualization/static_plots.py
:language: python
:linenos:
```

---

## Classes

### `ControlPlotter`

Static plotting utilities for control system analysis.

#### Source Code

```{literalinclude} ../../../src/utils/visualization/static_plots.py
:language: python
:pyobject: ControlPlotter
:linenos:
```

#### Methods (8)

##### `__init__(self, style, figsize)`

Initialize plotter with style settings.

[View full source →](#method-controlplotter-__init__)

##### `plot_time_series(self, time, data, title, ylabel, save_path)`

Plot multiple time series on the same axes.

[View full source →](#method-controlplotter-plot_time_series)

##### `plot_state_evolution(self, time, state_history, state_labels, save_path)`

Plot evolution of all state variables.

[View full source →](#method-controlplotter-plot_state_evolution)

##### `plot_phase_portrait(self, state_history, x_idx, y_idx, title, save_path)`

Plot phase portrait of two state variables.

[View full source →](#method-controlplotter-plot_phase_portrait)

##### `plot_control_performance(self, time, control_history, reference, save_path)`

Plot control input and reference tracking.

[View full source →](#method-controlplotter-plot_control_performance)

##### `plot_sliding_surface(self, time, sigma_history, boundary_layer, save_path)`

Plot sliding surface evolution for SMC analysis.

[View full source →](#method-controlplotter-plot_sliding_surface)

##### `plot_energy_analysis(self, time, kinetic_energy, potential_energy, total_energy, save_path)`

Plot system energy analysis.

[View full source →](#method-controlplotter-plot_energy_analysis)

##### `plot_performance_comparison(self, data_sets, metric_names, save_path)`

Plot performance comparison between different controllers.

[View full source →](#method-controlplotter-plot_performance_comparison)

---

### `SystemVisualization`

High-level visualization for complete system analysis.

#### Source Code

```{literalinclude} ../../../src/utils/visualization/static_plots.py
:language: python
:pyobject: SystemVisualization
:linenos:
```

#### Methods (2)

##### `__init__(self)`

Initialize system visualization.

[View full source →](#method-systemvisualization-__init__)

##### `create_complete_analysis_report(self, simulation_data, output_dir)`

Generate complete visualization report for system analysis.

[View full source →](#method-systemvisualization-create_complete_analysis_report)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import matplotlib.pyplot as plt`
- `import numpy as np`
- `from typing import List, Dict, Any, Optional, Tuple`
- `import matplotlib.patches as patches`
