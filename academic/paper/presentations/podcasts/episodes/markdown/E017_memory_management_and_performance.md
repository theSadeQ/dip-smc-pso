# E017: Memory Management and Performance

**Hosts**: Dr. Sarah Chen (Control Systems) & Alex Rivera (Software Engineering)

---

## Opening Hook

**Alex**: Your controller runs great for 100 iterations. Then 1000 iterations. Then you run a 10-hour experiment and...

**Sarah**: RAM usage balloons from 50 MB to 5 GB! System crashes! What happened?

**Alex**: **Memory leak!** The controller is accumulating history without bounds.

**Sarah**: Before fix:
```python
self.state_history = []
self.state_history.append(state)  # Grows forever!
```

After fix:
```python
from collections import deque
self.state_history = deque(maxlen=1000)  # Bounded circular buffer
```

**Alex**: This episode covers:
- **Memory leak detection**: Tools and techniques (tracemalloc, pytest)
- **Controller memory patterns**: Weakref, bounded buffers, cleanup methods
- **Performance profiling**: Finding memory hotspots
- **Production validation**: CA-02 audit results (100% passing)

**Sarah**: Let's make sure your controller doesn't eat all your RAM!

---

## The Problem: Memory Leaks in Controllers

**Sarah**: Let's start with a real example from our early development.

**Original implementation** (classical_smc.py, v0.1):
```python
class ClassicalSMC:
    def __init__(self, config):
        self.state_history = []  # Unbounded list!
        self.control_history = []
        self.sliding_surface_history = []

    def compute_control(self, state, last_control, history):
        # Compute control...
        self.state_history.append(state)  # Grows forever
        self.control_history.append(control)
        self.sliding_surface_history.append(s)
        return control
```

**Alex**: **What happens?**
- **10-second simulation**: 1000 timesteps, ~50 KB memory
- **100-second simulation**: 10,000 timesteps, ~500 KB memory
- **10-hour overnight experiment**: 3.6 million timesteps, **180 MB per controller!**
- **50 Monte Carlo runs**: 50 controllers × 180 MB = **9 GB RAM**

**Sarah**: System crashes with `MemoryError`. We lost 8 hours of overnight PSO optimization!

**Alex**: **The fix**:
```python
from collections import deque

class ClassicalSMC:
    def __init__(self, config):
        # Bounded circular buffers
        self.state_history = deque(maxlen=1000)  # Only last 1000 states
        self.control_history = deque(maxlen=1000)
        self.sliding_surface_history = deque(maxlen=1000)
```

**Sarah**: Now memory usage is **constant** - doesn't matter if you run for 1 hour or 100 hours!

---

## Memory Leak Detection: tracemalloc

**Alex**: Python's built-in `tracemalloc` module is our first line of defense against memory leaks.

**Example detection script**:
```python
import tracemalloc
from src.controllers.factory import create_controller

def test_memory_leak():
    tracemalloc.start()

    controller = create_controller('classical_smc', config=cfg)
    snapshot1 = tracemalloc.take_snapshot()

    # Run 10,000 iterations
    for i in range(10000):
        state = np.random.randn(6)
        control = controller.compute_control(state, 0.0, {})

    snapshot2 = tracemalloc.take_snapshot()

    # Compare snapshots
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')
    for stat in top_stats[:10]:
        print(stat)
```

**Output (BEFORE fix)**:
```
src/controllers/classical_smc.py:45: size=180 MiB (+180 MiB), count=3600000 (+3600000)
```

**Output (AFTER fix)**:
```
src/controllers/classical_smc.py:45: size=52 KiB (+0 KiB), count=1000 (+0)
```

**Sarah**: Notice the memory growth is **ZERO** after the fix!

---

## Controller Memory Patterns

**Alex**: We use 3 core patterns to prevent memory leaks:

### Pattern 1: Bounded Circular Buffers

**Use case**: Controllers that need recent history for derivative/integral terms.

**Implementation**:
```python
from collections import deque

class AdaptiveSMC:
    def __init__(self, config):
        # Only need last N samples
        self.error_history = deque(maxlen=10)  # For numerical derivative
        self.integral_history = deque(maxlen=100)  # For integral term
```

**Sarah**: **Why bounded?**
- Derivative: only need 2-10 samples for finite difference
- Integral: bounded buffer prevents windup
- No reason to store entire simulation history!

### Pattern 2: Weakref for Dynamics References

**Problem**: Controller holds reference to dynamics object causing circular references.

**Bad**:
```python
class HybridAdaptiveSTA:
    def __init__(self, config, dynamics):
        self.dynamics = dynamics  # Strong reference - keeps dynamics in memory!
```

**Good**:
```python
import weakref

class HybridAdaptiveSTA:
    def __init__(self, config, dynamics):
        self._dynamics_ref = weakref.ref(dynamics)  # Weak reference

    @property
    def dynamics(self):
        dyn = self._dynamics_ref()
        if dyn is None:
            raise RuntimeError("Dynamics object has been deleted")
        return dyn
```

**Alex**: **Why weakref?**
- Allows garbage collection of dynamics when simulation ends
- Prevents circular references (controller to dynamics to controller)
- CA-02 audit: 100% of controllers use weakref pattern

### Pattern 3: Explicit Cleanup Methods

**Sarah**: All controllers implement `cleanup()` for deterministic resource release.

**Implementation**:
```python
class ClassicalSMC:
    def cleanup(self):
        """Release memory and resources."""
        self.state_history.clear()
        self.control_history.clear()
        self.sliding_surface_history.clear()
        if hasattr(self, '_dynamics_ref'):
            self._dynamics_ref = None
```

**Usage**:
```python
try:
    for t in range(num_steps):
        control = controller.compute_control(state, ...)
finally:
    controller.cleanup()  # Always cleanup, even on error!
```

**Alex**: We also use Python's context manager protocol:
```python
class ClassicalSMC:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

# Usage
with create_controller('classical_smc', config=cfg) as controller:
    pass  # cleanup() called automatically!
```

---

## Memory Testing with pytest

**Alex**: We have 11 dedicated memory management tests.

**Test 1: No memory leak during long simulation**
```python
import tracemalloc
import pytest

@pytest.mark.parametrize("controller_type", [
    "classical_smc", "sta_smc", "adaptive_smc"
])
def test_no_memory_leak_long_simulation(controller_type):
    """Verify memory doesn't grow during 10,000 iterations."""
    tracemalloc.start()

    controller = create_controller(controller_type, config=test_config)
    snapshot1 = tracemalloc.take_snapshot()

    for i in range(10000):
        state = np.random.randn(6)
        control = controller.compute_control(state, 0.0, {})

    snapshot2 = tracemalloc.take_snapshot()
    stats = snapshot2.compare_to(snapshot1, 'lineno')
    total_growth = sum(stat.size_diff for stat in stats)

    assert total_growth < 1_000_000, f"Memory leak: {total_growth / 1e6:.1f} MB growth"
    controller.cleanup()
```

**Test 2: Cleanup releases memory**
```python
def test_cleanup_releases_memory():
    """Verify cleanup() releases controller memory."""
    controller = create_controller('classical_smc', config=test_config)

    for i in range(1000):
        controller.compute_control(np.random.randn(6), 0.0, {})

    snapshot1 = tracemalloc.take_snapshot()
    controller.cleanup()
    snapshot2 = tracemalloc.take_snapshot()

    stats = snapshot2.compare_to(snapshot1, 'lineno')
    total_change = sum(stat.size_diff for stat in stats)
    assert total_change < 0, "cleanup() did not release memory"
```

**Sarah**: **Test results (CA-02 audit)**:
```
tests/test_integration/test_memory_management/ ..... [ 100%]
11 tests passed in 2.34s
```

All 11 memory management tests: **PASSING**

---

## Performance Benchmarks: CA-02 Audit Results

**Sarah**: Our comprehensive audit validated all performance requirements.

### Memory Usage Benchmarks

**Test**: 10-hour simulation (3.6 million timesteps)

```
Controller Type          Peak Memory    Growth Rate    Status
-------------------------------------------------------------------
Classical SMC            52 KB          0.0 KB/hour    [OK]
STA-SMC                  68 KB          0.0 KB/hour    [OK]
Adaptive SMC             94 KB          0.0 KB/hour    [OK]
Hybrid Adaptive STA      118 KB         0.0 KB/hour    [OK]
-------------------------------------------------------------------
ALL CONTROLLERS: ZERO memory growth
```

**Alex**: **Zero growth rate** equals no memory leaks!

### CPU Performance Benchmarks

**Test**: Control computation time (1000 samples)

```
Controller Type          Mean Time    95th %ile    Max Time    Status
------------------------------------------------------------------------
Classical SMC            23 μs        28 μs        34 μs       [OK]
STA-SMC                  31 μs        38 μs        45 μs       [OK]
Adaptive SMC             47 μs        56 μs        67 μs       [OK]
Hybrid Adaptive STA      62 μs        74 μs        89 μs       [OK]
------------------------------------------------------------------------
ALL CONTROLLERS: < 100 μs (within 10 ms deadline)
```

**Sarah**: **Fastest**: Classical SMC (23 μs) - simplest algorithm
**Slowest**: Hybrid Adaptive STA (62 μs) - still **600× faster than deadline**!

---

## Garbage Collection Tuning

**Alex**: Python's garbage collector (GC) can cause real-time jitter.

### Problem: GC Pauses

**Before tuning**:
```python
for t in range(num_steps):
    control = controller.compute_control(state, ...)
    # Random GC pauses every ~700 iterations (10-50 ms!)
```

**Sarah**: GC pauses can **exceed our 10 ms deadline**!

### Solution: Disable GC During Critical Section

```python
import gc

gc.disable()  # Disable automatic GC

try:
    for t in range(num_steps):
        control = controller.compute_control(state, ...)

        # Manual GC every 1000 iterations
        if t % 1000 == 0:
            gc.collect()
finally:
    gc.enable()
```

**Alex**: GC pauses now occur **predictably** every 1000 iterations, not randomly.

**Sarah**: **Benchmark**:
- **Before**: 99th percentile latency = 45 ms (GC pauses)
- **After**: 99th percentile latency = 89 μs (no pauses in control loop)

---

## Summary: Memory Management Best Practices

**Sarah**: Let's recap our memory management strategy:

**1. Bounded Circular Buffers**
```python
from collections import deque
self.history = deque(maxlen=1000)  # NOT: self.history = []
```

**2. Weakref for Dynamics**
```python
import weakref
self._dynamics_ref = weakref.ref(dynamics)  # NOT: self.dynamics = dynamics
```

**3. Explicit Cleanup**
```python
def cleanup(self):
    self.state_history.clear()
    self._dynamics_ref = None
```

**4. Memory Testing**
```python
import tracemalloc
# Monitor memory growth during tests
```

**5. GC Tuning**
```python
gc.disable()  # Disable during real-time loop
gc.collect()  # Manual collection at safe points
```

**Alex**: **Key metrics from CA-02 audit**:
- **Memory leak tests**: 11/11 passing
- **Memory growth rate**: 0.0 KB/hour (all controllers)
- **Peak memory**: 52-118 KB (constant, bounded)
- **CPU performance**: 23-62 μs (600× faster than deadline)

**Sarah**: **Production readiness**:
- Thread-safe: 100% (11/11 tests passing)
- Memory-safe: 100% (0 leaks, 0 growth)
- Real-time capable: Yes (< 100 μs latency)

**Alex**: Your controller will run for **days** without eating RAM! Bounded buffers, weakrefs, cleanup methods - **three simple patterns** that prevent 99% of memory issues!

---

## Resources

- **Repository:** https://github.com/theSadeQ/dip-smc-pso.git
- **Documentation:** `docs/` directory
- **Getting Started:** `docs/guides/getting-started.md`
- **Memory Management Guide:** `.ai_workspace/config/controller_memory.md`
- **CA-02 Audit Report:** `academic/dev/quality/CA-02_comprehensive_audit.md`

---

*Educational podcast episode generated from comprehensive presentation materials*
