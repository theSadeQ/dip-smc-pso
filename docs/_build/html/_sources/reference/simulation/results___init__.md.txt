# simulation.results.__init__

**Source:** `src\simulation\results\__init__.py`

## Module Overview

Result processing and management for simulation framework.

## Complete Source Code

```{literalinclude} ../../../src/simulation/results/__init__.py
:language: python
:linenos:
```

---

## Dependencies

This module imports:

- `from .containers import StandardResultContainer, BatchResultContainer`
- `from .processors import ResultProcessor`
- `from .exporters import CSVExporter, HDF5Exporter`
- `from .validators import ResultValidator`
