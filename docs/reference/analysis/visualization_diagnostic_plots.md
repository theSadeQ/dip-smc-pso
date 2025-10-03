# analysis.visualization.diagnostic_plots

**Source:** `src\analysis\visualization\diagnostic_plots.py`

## Module Overview

Diagnostic visualization module for control system analysis.

This module provides specialized plotting capabilities for control system diagnostics,
including time-domain analysis, frequency-domain analysis, phase portraits,
and control performance visualization.

## Complete Source Code

```{literalinclude} ../../../src/analysis/visualization/diagnostic_plots.py
:language: python
:linenos:
```

---

## Classes

### `DiagnosticPlotter`

Specialized diagnostic plotting for control systems.

#### Source Code

```{literalinclude} ../../../src/analysis/visualization/diagnostic_plots.py
:language: python
:pyobject: DiagnosticPlotter
:linenos:
```

#### Methods (7)

##### `__init__(self, style, figsize)`

Initialize diagnostic plotter with control engineering styling.

[View full source →](#method-diagnosticplotter-__init__)

##### `_setup_style(self)`

Configure matplotlib style for control engineering plots.

[View full source →](#method-diagnosticplotter-_setup_style)

##### `plot_time_response(self, simulation_data, variables, title, save_path)`

Plot comprehensive time-domain response analysis.

[View full source →](#method-diagnosticplotter-plot_time_response)

##### `plot_phase_portrait(self, simulation_data, state_pairs, title, save_path)`

Create phase portrait plots for nonlinear system analysis.

[View full source →](#method-diagnosticplotter-plot_phase_portrait)

##### `plot_frequency_analysis(self, simulation_data, signal_indices, title, save_path)`

Perform frequency domain analysis of system signals.

[View full source →](#method-diagnosticplotter-plot_frequency_analysis)

##### `plot_control_performance(self, performance_metrics, title, save_path)`

Visualize control performance metrics.

[View full source →](#method-diagnosticplotter-plot_control_performance)

##### `_estimate_settling_time(self, time, signal, tolerance)`

Estimate settling time of a signal.

[View full source →](#method-diagnosticplotter-_estimate_settling_time)

---

## Dependencies

This module imports:

- `import matplotlib.pyplot as plt`
- `import numpy as np`
- `import pandas as pd`
- `from scipy import signal, fft`
- `from typing import Dict, List, Optional, Tuple, Any, Union`
- `import warnings`
- `from ..core.interfaces import DataProtocol`
- `from ..core.data_structures import SimulationData, PerformanceMetrics`
