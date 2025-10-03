# utils.control_analysis

**Source:** `src\utils\control_analysis.py`

## Module Overview

Control analysis utilities compatibility module.

This module provides backward compatibility for test modules that expect
control analysis utilities at src.utils.control_analysis. All functionality
is re-exported from the actual implementation location.

## Complete Source Code

```{literalinclude} ../../../src/utils/control_analysis.py
:language: python
:linenos:
```

---

## Dependencies

This module imports:

- `from ..analysis.performance.control_analysis import *`
- `from ..analysis.performance.control_analysis import ControlAnalyzer`
