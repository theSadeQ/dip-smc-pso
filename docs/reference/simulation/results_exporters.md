# simulation.results.exporters

**Source:** `src\simulation\results\exporters.py`

## Module Overview

Export simulation results to various formats.

## Complete Source Code

```{literalinclude} ../../../src/simulation/results/exporters.py
:language: python
:linenos:
```

---

## Classes

### `CSVExporter`

Export simulation results to CSV format.

#### Source Code

```{literalinclude} ../../../src/simulation/results/exporters.py
:language: python
:pyobject: CSVExporter
:linenos:
```

#### Methods (2)

##### `export(self, result_container, filepath)`

Export single simulation results to CSV.

[View full source →](#method-csvexporter-export)

##### `export_batch(self, batch_container, filepath)`

Export batch simulation results to CSV.

[View full source →](#method-csvexporter-export_batch)

---

### `HDF5Exporter`

Export simulation results to HDF5 format.

#### Source Code

```{literalinclude} ../../../src/simulation/results/exporters.py
:language: python
:pyobject: HDF5Exporter
:linenos:
```

#### Methods (2)

##### `export(self, result_container, filepath)`

Export single simulation results to HDF5.

[View full source →](#method-hdf5exporter-export)

##### `export_batch(self, batch_container, filepath)`

Export batch simulation results to HDF5.

[View full source →](#method-hdf5exporter-export_batch)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import csv`
- `from pathlib import Path`
- `from typing import Any`
- `import numpy as np`
