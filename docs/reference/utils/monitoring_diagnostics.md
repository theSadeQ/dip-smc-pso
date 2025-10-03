# utils.monitoring.diagnostics

**Source:** `src\utils\monitoring\diagnostics.py`

## Module Overview

Diagnostic checklist instrumentation for stability analysis.

Implements the 9-step diagnostic checklist from Issue #1 resolution plan
to systematically classify instability causes and provide actionable diagnosis.

## Complete Source Code

```{literalinclude} ../../../src/utils/monitoring/diagnostics.py
:language: python
:linenos:
```

---

## Classes

### `InstabilityType`

**Inherits from:** `Enum`

Classification of instability root causes.

#### Source Code

```{literalinclude} ../../../src/utils/monitoring/diagnostics.py
:language: python
:pyobject: InstabilityType
:linenos:
```

---

### `DiagnosticResult`

Result of a diagnostic check.

#### Source Code

```{literalinclude} ../../../src/utils/monitoring/diagnostics.py
:language: python
:pyobject: DiagnosticResult
:linenos:
```

---

### `DiagnosticChecklist`

9-step diagnostic checklist for systematic instability classification.

Implements the priority-ranked diagnostic checklist from Issue #1 resolution:
"Run top-down, stop at first fail"

#### Source Code

```{literalinclude} ../../../src/utils/monitoring/diagnostics.py
:language: python
:pyobject: DiagnosticChecklist
:linenos:
```

#### Methods (13)

##### `__init__(self, config)`

Initialize diagnostic checklist.

[View full source →](#method-diagnosticchecklist-__init__)

##### `run_full_diagnostic(self, episode_data)`

Run complete diagnostic checklist on episode data.

[View full source →](#method-diagnosticchecklist-run_full_diagnostic)

##### `_step1_reproduce_classify(self, step)`

Step 1: Reproduce & classify (baseline triage).

[View full source →](#method-diagnosticchecklist-_step1_reproduce_classify)

##### `_step2_numerical_conditioning(self, step)`

Step 2: Numerical conditioning gate.

[View full source →](#method-diagnosticchecklist-_step2_numerical_conditioning)

##### `_step3_actuator_authority(self, step)`

Step 3: Actuator authority & rate limits.

[View full source →](#method-diagnosticchecklist-_step3_actuator_authority)

##### `_step4_sliding_reachability(self, step)`

Step 4: Sliding reachability (Lyapunov trend).

[View full source →](#method-diagnosticchecklist-_step4_sliding_reachability)

##### `_step5_timing_noise(self, step)`

Step 5: Timing/latency/noise envelope.

[View full source →](#method-diagnosticchecklist-_step5_timing_noise)

##### `_step6_model_mismatch(self, step)`

Step 6: Model-mismatch A/B.

[View full source →](#method-diagnosticchecklist-_step6_model_mismatch)

##### `_step7_adaptation_safeguards(self, step)`

Step 7: Adaptation safeguards sanity.

[View full source →](#method-diagnosticchecklist-_step7_adaptation_safeguards)

##### `_step8_pso_objective(self, step)`

Step 8: PSO objective / distribution audit.

[View full source →](#method-diagnosticchecklist-_step8_pso_objective)

##### `_step9_mode_handoff(self, step)`

Step 9: Mode-handoff checks (if still unexplained).

[View full source →](#method-diagnosticchecklist-_step9_mode_handoff)

##### `_find_growth_onset(self, values, threshold_factor)`

Find the index where significant growth begins.

[View full source →](#method-diagnosticchecklist-_find_growth_onset)

##### `get_diagnostic_summary(self)`

Get summary of diagnostic results.

[View full source →](#method-diagnosticchecklist-get_diagnostic_summary)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from enum import Enum`
- `from typing import Dict, Any, List, Optional, Tuple`
- `import numpy as np`
- `import time`
- `from dataclasses import dataclass`
