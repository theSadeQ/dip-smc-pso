# PSO Parallel Mode - FIXED ✓

## Problem (RESOLVED)
Multiprocessing Pool.map could not serialize nested functions (closures).

**Error** (now fixed):
```
AttributeError: Can't get local object 'create_robust_cost_evaluator_wrapper.<locals>.cost_fn'
```

## Root Cause
The cost function was created as a closure inside `create_robust_cost_evaluator_wrapper()`, which Python's multiprocessing couldn't pickle for Windows (spawn mode).

## Solution Implemented ✓
**Option: Config file path + worker initialization**

Instead of passing the closure, we pass the config file path and recreate the evaluator in each worker process:

```python
# scripts/phase2_bulletproof_pso_v2.py
_GLOBAL_ROBUST_EVALUATOR = None

def _init_worker(controller_type: str, config_path: str):
    """Initialize worker process by creating RobustCostEvaluator."""
    global _GLOBAL_ROBUST_EVALUATOR
    config = load_config(config_path)  # Load config in worker
    # Create evaluator in this worker
    _GLOBAL_ROBUST_EVALUATOR = RobustCostEvaluator(...)

def _evaluate_particle_worker(gains: np.ndarray) -> float:
    """Top-level worker function (picklable)."""
    global _GLOBAL_ROBUST_EVALUATOR
    return _GLOBAL_ROBUST_EVALUATOR.evaluate_single_robust(gains)

def evaluate_particles_parallel(..., config_path="config.yaml"):
    """Parallel evaluation with proper Windows compatibility."""
    with Pool(processes=n_workers,
              initializer=_init_worker,
              initargs=(controller_type, config_path)) as pool:
        costs = pool.map(_evaluate_particle_worker, swarm_positions)
    return np.array(costs)
```

**Pros**:
- No external dependencies
- Windows compatible (spawn mode)
- Clean, no pickling errors
- Each worker has independent evaluator instance

**Cons**:
- Workers must load config from file (small overhead)
- Modest speedup on Windows (~1.5x due to spawn overhead vs 8x on Linux fork)

## Test Results ✓
```
Sequential time:  58.35 sec
Parallel time:    39.30 sec
Speedup:          1.48x (7 workers)
Cost verification: 0.000000 difference (perfect match!)
```

**Status**: FIXED and WORKING ✓

With **parallel + early termination + reduced sim time**, expected total speedup:
**Your 15 hours → 1-2 hours** (10-15x combined speedup)
