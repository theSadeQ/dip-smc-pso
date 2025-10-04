# interfaces.hil.data_logging

**Source:** `src\interfaces\hil\data_logging.py`

## Module Overview

Data logging system for HIL applications.
This module provides comprehensive data logging capabilities including
high-frequency data collection, buffering, compression, and export
for HIL system analysis and validation.

## Complete Source Code

```{literalinclude} ../../../src/interfaces/hil/data_logging.py
:language: python
:linenos:
```

---

## Classes

### `LogFormat`

**Inherits from:** `Enum`

Data logging format enumeration.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/data_logging.py
:language: python
:pyobject: LogFormat
:linenos:
```

---

### `CompressionType`

**Inherits from:** `Enum`

Data compression type enumeration.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/data_logging.py
:language: python
:pyobject: CompressionType
:linenos:
```

---

### `LoggingConfig`

HIL data logging configuration.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/data_logging.py
:language: python
:pyobject: LoggingConfig
:linenos:
```

---

### `LogEntry`

Individual log entry.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/data_logging.py
:language: python
:pyobject: LogEntry
:linenos:
```

---

### `HILDataLogger`

High-performance data logger for HIL systems.

Provides efficient data collection, buffering, and storage
with support for multiple formats and real-time compression.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/data_logging.py
:language: python
:pyobject: HILDataLogger
:linenos:
```

#### Methods (20)

##### `__init__(self, config)`

Initialize HIL data logger.

[View full source →](#method-hildatalogger-__init__)

##### `initialize(self)`

Initialize data logger.

[View full source →](#method-hildatalogger-initialize)

##### `start(self)`

Start data logging.

[View full source →](#method-hildatalogger-start)

##### `stop(self)`

Stop data logging.

[View full source →](#method-hildatalogger-stop)

##### `log_data(self, data, timestamp)`

Log data entry.

[View full source →](#method-hildatalogger-log_data)

##### `log_batch(self, batch_data)`

Log batch of data entries.

[View full source →](#method-hildatalogger-log_batch)

##### `get_statistics(self)`

Get logging statistics.

[View full source →](#method-hildatalogger-get_statistics)

##### `export_data(self, output_file, start_time, end_time, channels)`

Export logged data to file.

[View full source →](#method-hildatalogger-export_data)

##### `_flush_loop(self)`

Background flush loop.

[View full source →](#method-hildatalogger-_flush_loop)

##### `_flush_buffer(self)`

Flush buffer to file.

[View full source →](#method-hildatalogger-_flush_buffer)

##### `_write_entries(self, entries)`

Write entries to current file.

[View full source →](#method-hildatalogger-_write_entries)

##### `_write_hdf5_entries(self, entries)`

Write entries to HDF5 file.

[View full source →](#method-hildatalogger-_write_hdf5_entries)

##### `_write_csv_entries(self, entries)`

Write entries to CSV file.

[View full source →](#method-hildatalogger-_write_csv_entries)

##### `_write_json_entries(self, entries)`

Write entries to JSON file.

[View full source →](#method-hildatalogger-_write_json_entries)

##### `_create_new_file(self)`

Create new log file.

[View full source →](#method-hildatalogger-_create_new_file)

##### `_close_current_file(self)`

Close current log file.

[View full source →](#method-hildatalogger-_close_current_file)

##### `_rotate_file(self)`

Rotate to new log file.

[View full source →](#method-hildatalogger-_rotate_file)

##### `_cleanup_old_files(self)`

Clean up old log files.

[View full source →](#method-hildatalogger-_cleanup_old_files)

##### `_get_current_filename(self)`

Get current log filename.

[View full source →](#method-hildatalogger-_get_current_filename)

##### `_setup_output_directory(self)`

Setup output directory.

[View full source →](#method-hildatalogger-_setup_output_directory)

---

## Functions

### `load_hdf5_data(filepath, channels, start_time, end_time)`

Load data from HDF5 log file.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/data_logging.py
:language: python
:pyobject: load_hdf5_data
:linenos:
```

---

### `analyze_log_performance(log_stats)`

Analyze logging performance.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/data_logging.py
:language: python
:pyobject: analyze_log_performance
:linenos:
```

---

## Dependencies

This module imports:

- `import asyncio`
- `import time`
- `import csv`
- `import json`
- `import h5py`
- `import numpy as np`
- `from dataclasses import dataclass, field`
- `from typing import Dict, Any, Optional, List, Union, BinaryIO`
- `from enum import Enum`
- `import logging`

*... and 1 more*
