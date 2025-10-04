# analysis.visualization.__init__

**Source:** `src\analysis\visualization\__init__.py`

## Module Overview

Visualization module for control system analysis.

This module provides comprehensive visualization capabilities for analyzing
control system performance, validation results, and diagnostic information.

Components:
    - AnalysisPlotter: Main plotting interface for analysis results
    - StatisticalPlotter: Specialized statistical visualization
    - DiagnosticPlotter: Control system diagnostic plots
    - ReportGenerator: Automated report generation with plots

## Complete Source Code

```{literalinclude} ../../../src/analysis/visualization/__init__.py
:language: python
:linenos:
```

---

## Dependencies

This module imports:

- `from .analysis_plots import AnalysisPlotter`
- `from .statistical_plots import StatisticalPlotter`
- `from .diagnostic_plots import DiagnosticPlotter`
- `from .report_generator import ReportGenerator`
