# Phase 4 Production Hardening - Codex Handoff Instructions

**Date**: 2025-10-17
**Your Role**: Write production-grade thread safety tests
**Timeline**: Phase 4.2 (Days 6-8) + Phase 4.3 (Days 11-13) = 6 days total
**Estimated Effort**: 14-18 hours over 6 days
**Branch**: `phase4/production-hardening` (already created by Claude)

---

## Executive Summary

You will write **10-15 new thread safety tests** in Phase 4.2, then write **additional coverage tests** in Phase 4.3 to bring overall coverage from ~70-80% to ≥85%. Claude has already:

1. Fixed pytest execution issues (MEAS-001)
2. Collected coverage metrics (MEAS-002)
3. Fixed thread safety gaps (THREAD-001, THREAD-002)
4. Verified existing thread safety test suite passes (THREAD-003)

**Your job**: Write comprehensive thread safety tests for production scenarios that weren't covered by the existing test suite.

---

## Phase 4.2: Thread Safety Tests (Days 6-8)

**Your Tasks** (Priority Order):

### Task 1: Concurrent Controller Creation Tests (3 tests)

**File to Create**: `tests/test_integration/test_thread_safety/test_production_thread_safety.py`

**Test 1: 100 Simultaneous Classical SMC Creations**
```python
import pytest
import threading
import concurrent.futures
from src.controllers.factory import create_controller
from src.config import load_config

@pytest.mark.concurrent
class TestProductionThreadSafety:
    """Production-grade thread safety tests for real-world scenarios."""

    def test_concurrent_classical_smc_creation_100(self):
        """Test 100 simultaneous classical SMC controller creations."""
        config = load_config("config.yaml")
        controller_config = config.controllers.classical_smc

        def create_controller_task(task_id):
            """Create one controller instance."""
            try:
                controller = create_controller(
                    'classical_smc',
                    config=controller_config,
                    gains=[10.0, 5.0, 8.0, 3.0, 15.0, 2.0]
                )
                assert controller is not None, f"Task {task_id} failed to create controller"
                return True
            except Exception as e:
                print(f"Task {task_id} error: {e}")
                return False

        # Create 100 controllers concurrently
        num_tasks = 100
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(create_controller_task, i) for i in range(num_tasks)]
            results = [f.result(timeout=15) for f in concurrent.futures.as_completed(futures)]

        end_time = time.time()
        duration = end_time - start_time

        # Assertions
        assert all(results), f"Some controller creations failed: {results.count(False)}/{num_tasks}"
        assert duration < 10.0, f"Creation took too long: {duration:.2f}s (expected <10s)"
        print(f"SUCCESS: Created {num_tasks} controllers in {duration:.2f}s")
```

**Test 2: Mixed Controller Types (STA-SMC, Adaptive, Hybrid)**
```python
    def test_concurrent_mixed_controller_types(self):
        """Test concurrent creation of different controller types."""
        config = load_config("config.yaml")

        controller_types = [
            ('classical_smc', config.controllers.classical_smc),
            ('sta_smc', config.controllers.sta_smc),
            ('adaptive_smc', config.controllers.adaptive_smc),
            ('hybrid_adaptive_sta_smc', config.controllers.hybrid_adaptive_sta_smc)
        ]

        def create_mixed_controller(task_id):
            """Create controller of varying types."""
            ctrl_type, ctrl_config = controller_types[task_id % len(controller_types)]
            try:
                controller = create_controller(ctrl_type, config=ctrl_config)
                return {'success': True, 'type': ctrl_type, 'id': task_id}
            except Exception as e:
                return {'success': False, 'type': ctrl_type, 'id': task_id, 'error': str(e)}

        num_tasks = 80  # 20 of each type
        with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
            futures = [executor.submit(create_mixed_controller, i) for i in range(num_tasks)]
            results = [f.result(timeout=15) for f in concurrent.futures.as_completed(futures)]

        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]

        assert len(successful) >= 76, f"Too many failures: {len(failed)}/{num_tasks}"  # Allow 5% failure
        assert len(failed) == 0, f"Failures: {failed}"

        # Verify each type created successfully
        type_counts = {}
        for r in successful:
            type_counts[r['type']] = type_counts.get(r['type'], 0) + 1

        assert all(count >= 18 for count in type_counts.values()), f"Uneven type distribution: {type_counts}"
```

**Test 3: Rapid Create-Destroy Cycles (Memory Leak Check)**
```python
    def test_concurrent_create_destroy_cycles(self):
        """Test rapid controller creation and destruction for memory leaks."""
        import gc
        import psutil
        import os

        config = load_config("config.yaml")
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        def create_and_destroy_controller(task_id):
            """Create controller, use it, destroy it."""
            controller = create_controller('classical_smc', config=config.controllers.classical_smc)
            # Simulate usage
            state = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
            _ = controller.compute_control(state, None, None)
            del controller
            return True

        num_cycles = 1000
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(create_and_destroy_controller, i) for i in range(num_cycles)]
            results = [f.result(timeout=30) for f in concurrent.futures.as_completed(futures)]

        # Force garbage collection
        gc.collect()
        time.sleep(1)  # Allow cleanup

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        assert all(results), "Some create-destroy cycles failed"
        assert memory_increase < 50, f"Possible memory leak: {memory_increase:.1f}MB increase after {num_cycles} cycles"
        print(f"Memory usage: {initial_memory:.1f}MB -> {final_memory:.1f}MB (+{memory_increase:.1f}MB)")
```

---

### Task 2: PSO Multi-Threading Tests (2 tests)

**Test 4: PSO with Concurrent Fitness Evaluations**
```python
    def test_pso_concurrent_fitness_evaluations(self):
        """Test PSO optimizer with concurrent fitness evaluations."""
        from src.optimizer.pso_optimizer import PSOTuner
        from src.core.simulation_runner import run_simulation

        # Setup PSO tuner
        tuner = PSOTuner(
            controller_type='classical_smc',
            num_particles=10,
            num_iterations=5,
            num_workers=4  # Concurrent workers
        )

        def fitness_function(gains):
            """Fitness function that can be called concurrently."""
            # Simulate controller evaluation
            time.sleep(0.01)  # Simulate 10ms computation
            return np.sum(np.abs(gains))  # Simple fitness

        # Run PSO optimization
        start_time = time.time()
        best_gains, best_fitness = tuner.optimize(fitness_function)
        duration = time.time() - start_time

        assert best_gains is not None, "PSO optimization failed"
        assert best_fitness > 0, "Invalid fitness value"
        assert duration < 10.0, f"PSO took too long: {duration:.2f}s"
        print(f"PSO converged in {duration:.2f}s with fitness {best_fitness:.4f}")
```

**Test 5: PSO Particle Isolation**
```python
    def test_pso_particle_isolation(self):
        """Verify PSO particles don't interfere with each other's state."""
        from src.optimizer.pso_optimizer import PSOTuner

        tuner = PSOTuner(
            controller_type='classical_smc',
            num_particles=20,
            num_iterations=10,
            num_workers=10
        )

        particle_states = {}

        def fitness_with_tracking(gains):
            """Fitness function that tracks particle states."""
            thread_id = threading.current_thread().ident
            if thread_id not in particle_states:
                particle_states[thread_id] = []
            particle_states[thread_id].append(gains.copy())
            return np.sum(gains ** 2)

        best_gains, best_fitness = tuner.optimize(fitness_with_tracking)

        # Verify particles were isolated (different threads)
        assert len(particle_states) >= 5, f"Too few threads used: {len(particle_states)}"

        # Verify no particle state corruption
        for thread_id, states in particle_states.items():
            for i in range(len(states) - 1):
                # States should change over iterations (not stuck)
                assert not np.array_equal(states[i], states[i+1]), f"Particle {thread_id} state not updating"
```

---

### Task 3: Factory Registry Stress Tests (2 tests)

**Test 6: 1000 Concurrent Registry Reads**
```python
    def test_factory_registry_concurrent_reads_1000(self):
        """Test factory registry under heavy concurrent read load."""
        from src.controllers.factory.thread_safety import get_thread_safety_enhancement

        thread_safety = get_thread_safety_enhancement()
        # Initialize registry with some controllers
        test_registry = {
            'classical_smc': {'class': 'ClassicalSMC', 'file': 'classical_smc.py'},
            'sta_smc': {'class': 'STASMC', 'file': 'sta_smc.py'},
            'adaptive_smc': {'class': 'AdaptiveSMC', 'file': 'adaptive_smc.py'}
        }
        thread_safety.initialize_registry(test_registry)

        def concurrent_read(task_id):
            """Perform registry read."""
            ctrl_type = ['classical_smc', 'sta_smc', 'adaptive_smc'][task_id % 3]
            info = thread_safety.get_controller_info_safe(ctrl_type)
            return info is not None

        num_reads = 1000
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(concurrent_read, i) for i in range(num_reads)]
            results = [f.result(timeout=10) for f in concurrent.futures.as_completed(futures)]

        duration = time.time() - start_time

        assert all(results), "Some registry reads failed"
        assert duration < 2.0, f"Registry reads too slow: {duration:.2f}s (expected <2s)"
        print(f"Completed {num_reads} concurrent reads in {duration:.2f}s ({num_reads/duration:.0f} reads/sec)")
```

**Test 7: Mixed Read/Write Registry Operations**
```python
    def test_factory_registry_mixed_read_write(self):
        """Test registry with concurrent reads and occasional writes."""
        from src.controllers.factory.thread_safety import get_thread_safety_enhancement

        thread_safety = get_thread_safety_enhancement()
        initial_registry = {'classical_smc': {'class': 'ClassicalSMC'}}
        thread_safety.initialize_registry(initial_registry)

        read_count = [0]
        write_count = [0]
        lock = threading.Lock()

        def mixed_operation(task_id):
            """Perform read (90%) or write (10%) operation."""
            if task_id % 10 == 0:  # 10% writes
                new_registry = {
                    'classical_smc': {'class': 'ClassicalSMC'},
                    f'test_controller_{task_id}': {'class': f'TestCtrl{task_id}'}
                }
                thread_safety.lock_free_registry.update_registry(new_registry)
                with lock:
                    write_count[0] += 1
                return 'write'
            else:  # 90% reads
                info = thread_safety.get_controller_info_safe('classical_smc')
                with lock:
                    read_count[0] += 1
                return 'read' if info else 'fail'

        num_ops = 500
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(mixed_operation, i) for i in range(num_ops)]
            results = [f.result(timeout=10) for f in concurrent.futures.as_completed(futures)]

        reads = results.count('read')
        writes = results.count('write')
        fails = results.count('fail')

        assert fails == 0, f"Failed operations: {fails}"
        assert reads >= 400, f"Too few reads: {reads}"  # Expect ~450
        assert writes >= 40, f"Too few writes: {writes}"  # Expect ~50
        print(f"Completed {reads} reads, {writes} writes, {fails} fails")
```

---

### Task 4: Deadlock Scenario Tests (2 tests)

**Test 8: Controller Creation + PSO Optimization Concurrent**
```python
    def test_no_deadlock_creation_and_pso(self):
        """Test no deadlock when creating controllers while PSO runs."""
        from src.optimizer.pso_optimizer import PSOTuner
        import threading

        config = load_config("config.yaml")
        deadlock_detected = [False]
        timeout_seconds = 10

        def pso_worker():
            """Run PSO optimization."""
            try:
                tuner = PSOTuner(controller_type='classical_smc', num_particles=5, num_iterations=10)
                tuner.optimize(lambda gains: np.sum(gains ** 2))
            except Exception as e:
                print(f"PSO worker error: {e}")

        def creation_worker(task_id):
            """Create controllers concurrently."""
            try:
                controller = create_controller('classical_smc', config=config.controllers.classical_smc)
                return controller is not None
            except Exception as e:
                print(f"Creation worker {task_id} error: {e}")
                return False

        start_time = time.time()

        # Start PSO in background
        pso_thread = threading.Thread(target=pso_worker)
        pso_thread.start()

        # Create controllers concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(creation_worker, i) for i in range(50)]
            results = [f.result(timeout=timeout_seconds) for f in concurrent.futures.as_completed(futures)]

        # Wait for PSO to finish
        pso_thread.join(timeout=timeout_seconds)

        duration = time.time() - start_time

        # Check for deadlock
        if pso_thread.is_alive():
            deadlock_detected[0] = True
            pytest.fail(f"Possible deadlock: PSO thread still alive after {duration:.2f}s")

        assert all(results), f"Some creations failed: {results.count(False)}/50"
        assert duration < timeout_seconds, f"Operations took too long: {duration:.2f}s"
        print(f"No deadlock detected. Completed in {duration:.2f}s")
```

**Test 9: Multiple Factory Operations Deadlock Test**
```python
    def test_no_deadlock_multiple_factory_operations(self):
        """Test no deadlock with multiple factory operations simultaneously."""
        config = load_config("config.yaml")
        timeout_seconds = 8

        operations = ['create', 'get_info', 'list_controllers', 'create']

        def factory_operation(op_type, task_id):
            """Perform various factory operations."""
            try:
                if op_type == 'create':
                    ctrl_type = ['classical_smc', 'sta_smc'][task_id % 2]
                    controller = create_controller(ctrl_type, config=getattr(config.controllers, ctrl_type))
                    return 'created'

                elif op_type == 'get_info':
                    from src.controllers.factory import get_controller_info
                    info = get_controller_info('classical_smc')
                    return 'info' if info else 'no_info'

                elif op_type == 'list_controllers':
                    from src.controllers.factory import list_available_controllers
                    controllers = list_available_controllers()
                    return 'listed'

                return 'unknown'
            except Exception as e:
                return f'error: {e}'

        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for i in range(100):
                op_type = operations[i % len(operations)]
                futures.append(executor.submit(factory_operation, op_type, i))

            results = [f.result(timeout=timeout_seconds) for f in concurrent.futures.as_completed(futures)]

        duration = time.time() - start_time

        errors = [r for r in results if r.startswith('error')]
        assert len(errors) == 0, f"Factory operation errors: {errors[:5]}"
        assert duration < timeout_seconds, f"Possible deadlock: took {duration:.2f}s"
        print(f"All 100 factory operations completed in {duration:.2f}s without deadlock")
```

---

### Task 5: Memory Safety Under Concurrency (2 tests)

**Test 10: Check for Memory Leaks in 1000 Creation Cycles**
```python
    def test_memory_safety_1000_creation_cycles(self):
        """Test for memory leaks in 1000 concurrent controller creation cycles."""
        import gc
        import psutil
        import os

        config = load_config("config.yaml")
        process = psutil.Process(os.getpid())

        # Baseline memory
        gc.collect()
        time.sleep(0.5)
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        def create_use_destroy(task_id):
            """Create, use, destroy controller."""
            controller = create_controller('classical_smc', config=config.controllers.classical_smc)
            state = np.random.normal(0, 0.1, 6)
            _ = controller.compute_control(state, None, None)
            del controller
            return True

        num_cycles = 1000
        batch_size = 50

        for batch in range(num_cycles // batch_size):
            with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
                futures = [executor.submit(create_use_destroy, batch * batch_size + i) for i in range(batch_size)]
                results = [f.result(timeout=10) for f in concurrent.futures.as_completed(futures)]
                assert all(results), f"Batch {batch} had failures"

            # Periodic GC
            if batch % 5 == 0:
                gc.collect()

        # Final GC and measurement
        gc.collect()
        time.sleep(0.5)
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        assert memory_increase < 100, f"Memory leak detected: {memory_increase:.1f}MB increase after {num_cycles} cycles"
        print(f"Memory: {initial_memory:.1f}MB -> {final_memory:.1f}MB (+{memory_increase:.1f}MB) for {num_cycles} cycles")
```

**Test 11: Verify Weakref Cleanup in Concurrent Scenarios**
```python
    def test_weakref_cleanup_concurrent(self):
        """Verify weakref cleanup works correctly in concurrent controller creation."""
        import weakref
        import gc

        config = load_config("config.yaml")
        weak_refs = []
        lock = threading.Lock()

        def create_and_track_controller(task_id):
            """Create controller and track with weakref."""
            controller = create_controller('classical_smc', config=config.controllers.classical_smc)
            weak_ref = weakref.ref(controller)

            with lock:
                weak_refs.append(weak_ref)

            # Use controller briefly
            state = np.random.normal(0, 0.05, 6)
            _ = controller.compute_control(state, None, None)

            del controller  # Explicit deletion
            return True

        num_controllers = 200
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(create_and_track_controller, i) for i in range(num_controllers)]
            results = [f.result(timeout=15) for f in concurrent.futures.as_completed(futures)]

        assert all(results), "Some controller creations failed"

        # Force garbage collection
        gc.collect()
        time.sleep(1)

        # Check weakrefs are dead
        alive_refs = [ref for ref in weak_refs if ref() is not None]
        alive_count = len(alive_refs)

        assert alive_count == 0, f"Weakref cleanup failed: {alive_count}/{num_controllers} controllers still alive"
        print(f"All {num_controllers} weakrefs successfully cleaned up")
```

---

## Your File (Create This)

**File**: `tests/test_integration/test_thread_safety/test_production_thread_safety.py`

**Template Structure**:
```python
#==========================================================================================\\\
#== tests/test_integration/test_thread_safety/test_production_thread_safety.py ============\\\
#==========================================================================================\\\

"""
Production Thread Safety Tests - Phase 4.2 (Codex-Written)

Comprehensive thread safety tests for production scenarios:
- 100+ concurrent controller creations
- PSO multi-threading validation
- Factory registry stress tests
- Deadlock detection
- Memory leak prevention
"""

import pytest
import numpy as np
import threading
import time
import concurrent.futures
import gc
import psutil
import os
from typing import List, Dict, Any

@pytest.mark.concurrent
class TestProductionThreadSafety:
    """Production-grade thread safety tests."""

    # Test 1: 100 Simultaneous Classical SMC Creations
    def test_concurrent_classical_smc_creation_100(self):
        # ... (see above)

    # Test 2: Mixed Controller Types
    def test_concurrent_mixed_controller_types(self):
        # ... (see above)

    # Test 3: Create-Destroy Cycles
    def test_concurrent_create_destroy_cycles(self):
        # ... (see above)

    # Test 4: PSO Concurrent Fitness
    def test_pso_concurrent_fitness_evaluations(self):
        # ... (see above)

    # Test 5: PSO Particle Isolation
    def test_pso_particle_isolation(self):
        # ... (see above)

    # Test 6: 1000 Concurrent Reads
    def test_factory_registry_concurrent_reads_1000(self):
        # ... (see above)

    # Test 7: Mixed Read/Write
    def test_factory_registry_mixed_read_write(self):
        # ... (see above)

    # Test 8: No Deadlock (Creation + PSO)
    def test_no_deadlock_creation_and_pso(self):
        # ... (see above)

    # Test 9: No Deadlock (Multiple Factory Ops)
    def test_no_deadlock_multiple_factory_operations(self):
        # ... (see above)

    # Test 10: Memory Leaks
    def test_memory_safety_1000_creation_cycles(self):
        # ... (see above)

    # Test 11: Weakref Cleanup
    def test_weakref_cleanup_concurrent(self):
        # ... (see above)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-m", "concurrent"])
```

---

## Validation Checklist

Before considering Task 1 complete:

- [ ] File created: `tests/test_integration/test_thread_safety/test_production_thread_safety.py`
- [ ] All 11 tests implemented
- [ ] All tests use `@pytest.mark.concurrent` marker
- [ ] Run tests: `pytest tests/test_integration/test_thread_safety/test_production_thread_safety.py -v`
- [ ] All 11 tests PASS
- [ ] Commit with message: `test(thread-safety): Add 11 production thread safety tests for Phase 4.2`

---

## Phase 4.3: Coverage Improvement Tests (Days 11-13)

**Your Task**: Write additional tests to bring overall coverage from ~75-80% to ≥85%

### Step 1: Identify Coverage Gaps (Claude Will Provide This)

Claude will run:
```bash
pytest --cov=src --cov-report=html
# Check htmlcov/index.html for uncovered modules
```

Claude will then provide you with a list like:
```
Uncovered modules (need tests):
1. src/controllers/classical_smc.py - Lines 45-52, 78-85 (edge cases)
2. src/optimizer/pso_optimizer.py - Lines 123-135 (error handling)
3. src/controllers/factory/core.py - Lines 67-74 (rare paths)
```

### Step 2: Write Tests for Gaps

You'll create test files as directed by Claude:
- `tests/test_controllers/test_classical_smc_extended.py` (if needed)
- `tests/test_optimizer/test_pso_edge_cases.py` (if needed)
- `tests/test_factory/test_factory_edge_cases.py` (if needed)

### Step 3: Verify Coverage Improvement

```bash
pytest --cov=src --cov-report=term
# Verify overall coverage ≥85%
```

---

## File Ownership (Important!)

**You Own (create/modify)**:
- `tests/test_integration/test_thread_safety/test_production_thread_safety.py` (Phase 4.2)
- Any test files Claude directs you to create (Phase 4.3)

**Claude Owns (read-only for you)**:
- `src/controllers/factory/thread_safety.py`
- `src/integration/production_readiness.py`
- `.project/ai/planning/phase4/*.md`
- `tests/test_integration/test_thread_safety/test_concurrent_thread_safety_deep.py`

**Do NOT modify Claude's files!** This prevents merge conflicts.

---

## Dependencies (Wait for These)

**Before starting Phase 4.2**:
- [ ] Claude completes MEAS-001 (pytest execution fixed)
- [ ] Claude completes MEAS-002 (coverage metrics collected)
- [ ] Claude completes THREAD-001 (atomic counter fix)
- [ ] Claude completes THREAD-002 (singleton refactor)
- [ ] Claude completes THREAD-003 (existing tests pass)

**You'll know it's ready when**:
```bash
# This command should work without errors:
pytest tests/test_integration/test_thread_safety/test_concurrent_thread_safety_deep.py -v
# Expected: 8/8 tests PASSED
```

---

## Commit Guidelines

**Commit Message Format**:
```
test(thread-safety): <Brief description>

<Details about what tests were added>

Resolves: THREAD-004 (Phase 4.2)

[AI] Generated with Codex
```

**Example**:
```
test(thread-safety): Add 11 production thread safety tests

Added comprehensive thread safety tests for:
- 100+ concurrent controller creations (3 tests)
- PSO multi-threading validation (2 tests)
- Factory registry stress tests (2 tests)
- Deadlock detection scenarios (2 tests)
- Memory leak prevention (2 tests)

All tests pass with 0 failures.

Resolves: THREAD-004 (Phase 4.2)

[AI] Generated with Codex
```

---

## Communication

**Report to User**:
1. When you start Phase 4.2 (Day 6)
2. After completing test file (Day 8)
3. When all tests pass
4. If you encounter any failures or need Claude's help

**Update Progress**:
- Commit your work frequently
- Push to `phase4/production-hardening` branch
- Claude will monitor via git log

---

## Success Criteria (Your Part)

**Phase 4.2 Complete When**:
- [ ] 11 production thread safety tests written
- [ ] File: `test_production_thread_safety.py` exists and committed
- [ ] Run: `pytest tests/test_integration/test_thread_safety/test_production_thread_safety.py -v`
- [ ] Result: 11/11 tests PASSED
- [ ] Commit pushed to `phase4/production-hardening` branch

**Phase 4.3 Complete When**:
- [ ] Additional coverage tests written (as directed by Claude)
- [ ] Run: `pytest --cov=src --cov-report=term`
- [ ] Result: Overall coverage ≥85%
- [ ] Commit pushed to `phase4/production-hardening` branch

---

## Questions?

If you encounter issues:
1. Check existing test file: `tests/test_integration/test_thread_safety/test_concurrent_thread_safety_deep.py` (use as reference)
2. Verify dependencies fixed (run `pytest tests/test_integration/test_thread_safety/test_concurrent_thread_safety_deep.py -v`)
3. Report to user with error details

---

**Document Version**: 1.0
**Last Updated**: 2025-10-17
**Status**: Handoff ready | Awaiting Claude's completion of THREAD-001/002/003
**Your Start Date**: TBD (after Claude completes Phase 4.2 prerequisites, ~Day 6)
