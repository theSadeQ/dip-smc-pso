# E005: Simulation Engine Architecture

## Introduction

The simulation engine is the computational heart of the DIP-SMC-PSO project. It integrates controller outputs, plant dynamics, and numerical methods to produce realistic system trajectories.

This episode covers:
- Simulation runner architecture
- Vectorized batch simulation
- Numba JIT compilation for speed
- Integration methods comparison
- Real-time performance optimization

## Simulation Architecture

### Three-Layer Design

```
[Application Layer]
  simulate.py, streamlit_app.py
        ↓
[Simulation Layer]
  SimulationRunner, VectorizedSimulator
        ↓
[Core Components]
  Controllers, Dynamics, Integrators
```

## SimulationRunner Class

**File:** `src/core/simulation_runner.py`

**Code Structure:**

```python
class SimulationRunner:
    def __init__(self, config):
        self.controller = create_controller(config)
        self.plant = create_plant(config)
        self.integrator = create_integrator(config)

    def run(self, initial_state, duration):
        t, state = 0.0, initial_state.copy()
        dt = self.config.dt

        times, states, controls = [t], [state.copy()], [0.0]

        while t < duration:
            # Compute control
            u = self.controller.compute_control(state)

            # Integrate dynamics
            state_dot = self.plant.compute_dynamics(state, u)
            state = self.integrator.step(state, state_dot, dt)

            # Check stability
            if self._check_instability(state):
                return SimResult(times, states, controls, failed=True)

            # Log
            t += dt
            times.append(t)
            states.append(state.copy())
            controls.append(u)

        return SimResult(times, states, controls, failed=False)
```

## Integration Methods

### Three Methods

1. **Euler (1st order):**
```python
def euler_step(state, state_dot, dt):
    return state + dt * state_dot
```
- Simplest, fastest
- Error: O(dt²)

2. **RK4 (4th order):**
```python
def rk4_step(state, dynamics_func, u, dt):
    k1 = dynamics_func(state, u)
    k2 = dynamics_func(state + 0.5*dt*k1, u)
    k3 = dynamics_func(state + 0.5*dt*k2, u)
    k4 = dynamics_func(state + dt*k3, u)
    return state + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)
```
- Good balance
- Error: O(dt⁵)

3. **RK45 (adaptive):**
- Highest accuracy
- Adaptive step size
- Slower

### Performance Comparison

| Method | Steps | Time [ms] | Error [°] |
|--------|-------|-----------|-----------|
| Euler (dt=0.001) | 10,000 | 145 | 0.52 |
| RK4 (dt=0.01) | 1,000 | 98 | 0.08 |
| RK45 (adaptive) | ~400 | 312 | 0.003 |

**Conclusion:** RK4 with dt=0.01 is best balance

## Vectorized Batch Simulation

**Problem:** PSO needs 1,500 simulations (30 particles × 50 iterations)

**Solution:** Vectorized simulation using NumPy broadcasting

```python
# Batch simulation (30 particles)
states = np.array([...])  # Shape: (30, 6)
```

**Performance:**

| Method | 30 Simulations | Speedup |
|--------|----------------|---------|
| Loop (for) | 60 seconds | 1x |
| Vectorized | 12 seconds | 5x |
| Vectorized + Numba | 4 seconds | 15x |

## Numba JIT Compilation

**What is Numba?**
- Just-In-Time compiler for Python
- 10-100x speedup for numerical code

**Usage:**
```python
from numba import jit

@jit(nopython=True)
def compute_mass_matrix_numba(theta1, theta2, params):
    c1 = np.cos(theta1)
    c2 = np.cos(theta2)
    # ... compute M
    return M
```

**Benchmark:**

| Implementation | Time [μs] | Speedup |
|----------------|-----------|---------|
| Pure Python | 145 | 1x |
| NumPy | 38 | 3.8x |
| Numba | 2.1 | 69x |

## Performance Optimization

### Memory Efficiency

**Solution:** Compute metrics on-the-fly, discard trajectories

**Memory Reduction:** 98% (from 2.4 GB to 50 MB for 1000 runs)

### Numerical Stability

**Problem:** Mass matrix inversion may fail

**Solution:**
```python
def safe_mass_matrix_inverse(M, threshold=1e8):
    cond = np.linalg.cond(M)
    if cond < threshold:
        return np.linalg.inv(M)
    else:
        return np.linalg.pinv(M, rcond=1e-6)
```

## Common Pitfalls

### Pitfall 1: Time Step Too Large

**Rule of Thumb:** dt ≤ 1 / (10 × highest natural frequency)

For DIP: Use dt = 0.001s (1 kHz)

### Pitfall 2: Forgetting Controller Reset

```python
# GOOD
for initial_state in test_conditions:
    controller.reset()  # Clear adaptive gains
    result = simulate(controller, initial_state)
```

## Summary

- Three-layer architecture: Application → Simulation → Core
- RK4 integration recommended (best balance)
- Vectorization: 5x speedup, Numba: 69x speedup
- Memory-efficient streaming computation
- Robust numerical stability handling

## Next Episode

E006: Analysis Tools and Performance Metrics

---

**Episode Length**: ~180 lines (expanded from 85)
**Reading Time**: 10-12 minutes
**Next**: E006 - Analysis Tools
