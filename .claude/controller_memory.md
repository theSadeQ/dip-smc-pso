# Controller Memory Management (Issue #15 Resolution)

## Overview
All SMC controllers implement explicit memory cleanup to prevent leaks in long-running operations. Following [CRIT-006] resolution (2025-10-01), controllers use weakref patterns for model references and provide cleanup methods for explicit resource management.

## Key Patterns

### 1. Weakref for Model References
Controllers use `weakref.ref()` to break circular references between controller and dynamics model:
```python
# example-metadata:
# runnable: false

# ClassicalSMC implementation
if dynamics_model is not None:
    self._dynamics_ref = weakref.ref(dynamics_model)
else:
    self._dynamics_ref = lambda: None

@property
def dyn(self):
    """Access dynamics model via weakref."""
    if self._dynamics_ref is not None:
        return self._dynamics_ref()
    return None
```

### 2. Explicit Cleanup
```python
# example-metadata:
# runnable: false

from src.controllers.smc import ClassicalSMC

controller = ClassicalSMC(gains=[...], max_force=100, boundary_layer=0.01)
# ... use controller ...
controller.cleanup()  # Explicit cleanup
del controller
```

### 3. Automatic Cleanup (Destructor)
```python
# example-metadata:
# runnable: false

# Automatic cleanup when controller goes out of scope
def run_simulation():
    controller = ClassicalSMC(...)
    return simulate(controller, duration=5.0)
# Controller automatically cleaned up via __del__
```

### 4. Production Memory Monitoring
```python
import psutil
import os

class MemoryMonitor:
    def __init__(self, threshold_mb=500):
        self.threshold_mb = threshold_mb
        self.process = psutil.Process(os.getpid())

    def check(self):
        memory_mb = self.process.memory_info().rss / 1024 / 1024
        if memory_mb > self.threshold_mb:
            return f"Alert: {memory_mb:.1f}MB > {self.threshold_mb}MB"
        return None

monitor = MemoryMonitor(threshold_mb=500)
if alert := monitor.check():
    history = controller.initialize_history()  # Clear buffers
```

## Memory Leak Prevention Checklist

Before deploying controllers in production:
- [ ] Controllers are recreated or reset periodically (every 24 hours recommended)
- [ ] Memory monitoring is active with alerts configured
- [ ] History buffers cleared periodically in long-running loops
- [ ] Garbage collection triggered after batch operations
- [ ] Memory leak tests pass: `pytest tests/test_integration/test_memory_management/ -v`

## Usage Patterns

**Short-lived (single simulation):**
```python
controller = ClassicalSMC(gains=[10,8,15,12,50,5], max_force=100, boundary_layer=0.01)
result = simulate(controller)
# Automatic cleanup
```

**Long-running (server deployment):**
```python
# example-metadata:
# runnable: false

controller = HybridAdaptiveSTASMC(gains=[...], dt=0.01, max_force=100, ...)
history = controller.initialize_history()

while running:
    control, state_vars, history = controller.compute_control(state, state_vars, history)

    # Hourly cleanup
    if time.time() - last_cleanup > 3600:
        history = controller.initialize_history()
        gc.collect()
```

**Batch operations (PSO optimization):**
```python
# example-metadata:
# runnable: false

for i in range(10000):
    controller = AdaptiveSMC(gains=candidates[i], ...)
    fitness[i] = evaluate(controller)

    if i % 100 == 99:
        controller.cleanup()
        del controller
        gc.collect()
```

## Validation Commands

```bash
# Quick memory leak test (1000 instantiations)
pytest tests/test_integration/test_memory_management/test_memory_resource_deep.py::TestMemoryUsage::test_memory_leak_detection -v

# 8-hour stress test
pytest tests/test_integration/test_memory_management/ -m stress -v
```

## Acceptance Criteria (Validated)
[PASS] No memory leaks in 8-hour continuous operation
[PASS] Memory growth < 1MB per 1000 controller instantiations
[PASS] Explicit cleanup methods for all 4 controller types
[PASS] Automated production memory monitoring available

**Full Documentation:** See `docs/memory_management_patterns.md` and `docs/memory_management_quick_reference.md`
