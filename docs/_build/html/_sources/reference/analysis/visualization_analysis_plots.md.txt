# analysis.visualization.analysis_plots

**Source:** `src\analysis\visualization\analysis_plots.py`

## Module Overview

Analysis visualization tools for control engineering applications.

This module provides comprehensive visualization capabilities for analysis results
including performance plots, comparison charts, and interactive visualizations.

## Complete Source Code

```{literalinclude} ../../../src/analysis/visualization/analysis_plots.py
:language: python
:linenos:
```

---

## Classes

### `AnalysisPlotter`

**Inherits from:** `VisualizationGenerator`

Professional analysis plotting framework.

#### Source Code

```{literalinclude} ../../../src/analysis/visualization/analysis_plots.py
:language: python
:pyobject: AnalysisPlotter
:linenos:
```

#### Methods (42)

##### `__init__(self, style, figsize, dpi, color_palette)`

Initialize analysis plotter.

[View full source →](#method-analysisplotter-__init__)

##### `_setup_style(self)`

Setup matplotlib style for professional plots.

[View full source →](#method-analysisplotter-_setup_style)

##### `supported_formats(self)`

List of supported output formats.

[View full source →](#method-analysisplotter-supported_formats)

##### `generate(self, analysis_result)`

Generate visualization from analysis results.

[View full source →](#method-analysisplotter-generate)

##### `create_summary_plot(self, analysis_result, output_path)`

Create comprehensive summary plot.

[View full source →](#method-analysisplotter-create_summary_plot)

##### `create_performance_comparison(self, analysis_result, output_path)`

Create performance comparison visualization.

[View full source →](#method-analysisplotter-create_performance_comparison)

##### `create_time_series_plot(self, analysis_result, output_path)`

Create time series analysis plot.

[View full source →](#method-analysisplotter-create_time_series_plot)

##### `create_distribution_plot(self, analysis_result, output_path)`

Create distribution analysis plot.

[View full source →](#method-analysisplotter-create_distribution_plot)

##### `create_correlation_matrix(self, analysis_result, output_path)`

Create correlation matrix visualization.

[View full source →](#method-analysisplotter-create_correlation_matrix)

##### `create_control_performance_plot(self, analysis_result, output_path)`

Create control-specific performance visualization.

[View full source →](#method-analysisplotter-create_control_performance_plot)

##### `_plot_key_metrics(self, ax, data)`

Plot key metrics as bar chart.

[View full source →](#method-analysisplotter-_plot_key_metrics)

##### `_plot_performance_trends(self, ax, data)`

Plot performance trends over time or iterations.

[View full source →](#method-analysisplotter-_plot_performance_trends)

##### `_plot_distribution_overview(self, ax, data)`

Plot distribution overview.

[View full source →](#method-analysisplotter-_plot_distribution_overview)

##### `_plot_quality_indicators(self, ax, data)`

Plot quality indicators as gauge-style visualization.

[View full source →](#method-analysisplotter-_plot_quality_indicators)

##### `_plot_metric_comparison(self, ax, data)`

Plot metric comparison between methods.

[View full source →](#method-analysisplotter-_plot_metric_comparison)

##### `_plot_statistical_significance(self, ax, data)`

Plot statistical significance results.

[View full source →](#method-analysisplotter-_plot_statistical_significance)

##### `_plot_effect_sizes(self, ax, data)`

Plot effect sizes.

[View full source →](#method-analysisplotter-_plot_effect_sizes)

##### `_plot_time_series_data(self, ax, data)`

Plot time series data.

[View full source →](#method-analysisplotter-_plot_time_series_data)

##### `_plot_residuals_analysis(self, ax, data)`

Plot residuals analysis.

[View full source →](#method-analysisplotter-_plot_residuals_analysis)

##### `_plot_frequency_analysis(self, ax, data)`

Plot frequency domain analysis.

[View full source →](#method-analysisplotter-_plot_frequency_analysis)

##### `_plot_histogram_with_fit(self, ax, data)`

Plot histogram with distribution fit.

[View full source →](#method-analysisplotter-_plot_histogram_with_fit)

##### `_plot_qq_plot(self, ax, data)`

Plot Q-Q plot for normality assessment.

[View full source →](#method-analysisplotter-_plot_qq_plot)

##### `_plot_box_plot_analysis(self, ax, data)`

Plot box plot with outlier analysis.

[View full source →](#method-analysisplotter-_plot_box_plot_analysis)

##### `_plot_density_comparison(self, ax, data)`

Plot probability density comparison.

[View full source →](#method-analysisplotter-_plot_density_comparison)

##### `_plot_correlation_heatmap(self, ax, data)`

Plot correlation heatmap.

[View full source →](#method-analysisplotter-_plot_correlation_heatmap)

##### `_plot_correlation_network(self, ax, data)`

Plot correlation network diagram.

[View full source →](#method-analysisplotter-_plot_correlation_network)

##### `_plot_step_response_analysis(self, ax, data)`

Plot step response analysis.

[View full source →](#method-analysisplotter-_plot_step_response_analysis)

##### `_plot_frequency_response(self, ax, data)`

Plot frequency response.

[View full source →](#method-analysisplotter-_plot_frequency_response)

##### `_plot_stability_margins(self, ax, data)`

Plot stability margins.

[View full source →](#method-analysisplotter-_plot_stability_margins)

##### `_plot_control_effort_analysis(self, ax, data)`

Plot control effort analysis.

[View full source →](#method-analysisplotter-_plot_control_effort_analysis)

##### `_plot_robustness_analysis(self, ax, data)`

Plot robustness analysis.

[View full source →](#method-analysisplotter-_plot_robustness_analysis)

##### `_plot_performance_radar(self, ax, data)`

Plot performance radar chart.

[View full source →](#method-analysisplotter-_plot_performance_radar)

##### `_extract_metrics_from_data(self, data)`

Extract metrics from analysis data.

[View full source →](#method-analysisplotter-_extract_metrics_from_data)

##### `_extract_time_series_from_data(self, data)`

Extract time series data.

[View full source →](#method-analysisplotter-_extract_time_series_from_data)

##### `_extract_distribution_data(self, data)`

Extract data for distribution analysis.

[View full source →](#method-analysisplotter-_extract_distribution_data)

##### `_extract_quality_metrics(self, data)`

Extract quality metrics.

[View full source →](#method-analysisplotter-_extract_quality_metrics)

##### `_extract_comparison_data(self, data)`

Extract comparison data between methods.

[View full source →](#method-analysisplotter-_extract_comparison_data)

##### `_extract_significance_data(self, data)`

Extract statistical significance data.

[View full source →](#method-analysisplotter-_extract_significance_data)

##### `_extract_effect_size_data(self, data)`

Extract effect size data.

[View full source →](#method-analysisplotter-_extract_effect_size_data)

##### `_extract_residuals_data(self, data)`

Extract residuals data.

[View full source →](#method-analysisplotter-_extract_residuals_data)

##### `_extract_frequency_data(self, data)`

Extract frequency domain data.

[View full source →](#method-analysisplotter-_extract_frequency_data)

##### `_extract_correlation_data(self, data)`

Extract correlation matrix data.

[View full source →](#method-analysisplotter-_extract_correlation_data)

---

## Functions

### `create_analysis_plotter(style)`

Factory function to create analysis plotter.

Parameters
----------
style : str, optional
    Plot style
**kwargs
    Additional configuration parameters

Returns
-------
AnalysisPlotter
    Configured analysis plotter

#### Source Code

```{literalinclude} ../../../src/analysis/visualization/analysis_plots.py
:language: python
:pyobject: create_analysis_plotter
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Dict, List, Optional, Tuple, Any, Union`
- `import numpy as np`
- `import matplotlib.pyplot as plt`
- `import matplotlib.patches as patches`
- `from matplotlib.patches import Ellipse`
- `from scipy import stats`
- `import warnings`
- `from pathlib import Path`
- `from ..core.interfaces import VisualizationGenerator, AnalysisResult`

*... and 1 more*
