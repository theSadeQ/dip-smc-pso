# Quick Layer Reference Guide

> Fast lookup for layered learning roadmap navigation

**See Full Roadmap:** `.ai_workspace/edu/layered-learning-roadmap.md`

---

## Which Layer Do I Need?

- Run simulations and modify parameters -> Layer 1
- Understand the simulation engine -> Layer 2
- Implement custom controllers or optimization -> Layer 3
- Deploy to production or conduct research -> Layer 4
- Extend the framework or lead development -> Layer 5

---

## Layer Quick Reference

### Layer 1: Foundation (15-20 hrs)
**Who:** Beginners
**Focus:** Running simulations, basic usage
**Key Files:** `simulate.py`, `config.yaml`, controller interfaces
**Checkpoint:** Can run 5 different simulations

### Layer 2: Core Mechanics (25-35 hrs)
**Who:** Intermediate users
**Focus:** Plant dynamics, simulation engine
**Key Files:** `src/plant/`, `src/simulation/`, integrators
**Checkpoint:** Can explain DIP equations and debug failures

### Layer 3: Advanced Control (35-50 hrs)
**Who:** Control engineers, researchers
**Focus:** SMC variants, PSO optimization
**Key Files:** `src/controllers/`, `src/optimization/`, analysis tools
**Checkpoint:** Can design custom controller and run PSO

### Layer 4: Integration (40-60 hrs)
**Who:** Senior engineers
**Focus:** HIL, statistical validation, production
**Key Files:** `src/interfaces/`, `src/analysis/validation/`, `src/integration/`
**Checkpoint:** Can conduct Monte Carlo study and deploy system

### Layer 5: Mastery (50-80 hrs)
**Who:** Framework architects
**Focus:** Complete ecosystem understanding
**Key Files:** All remaining modules
**Checkpoint:** Can extend framework and mentor contributors

---

## File-to-Layer Lookup (Verified Paths)

### Core Entry Points
- `simulate.py` -> Layer 1 (main CLI)
- `config.yaml` -> Layer 1 (configuration)
- `streamlit_app.py` -> Layer 2 (web UI)

### Controllers
- `src/controllers/base/controller_interface.py` -> Layer 1 (interface)
- `src/controllers/smc/algorithms/classical/` -> Layer 1 (classical SMC)
- `src/controllers/smc/algorithms/super_twisting/` -> Layer 3 (advanced)
- `src/controllers/smc/algorithms/adaptive/` -> Layer 3 (adaptive)
- `src/controllers/smc/algorithms/hybrid/` -> Layer 3 (hybrid)
- `src/controllers/factory/` -> Layer 3 (factory pattern)

### Plant Models
- `src/plant/models/simplified/dynamics.py` -> Layer 2 (simplified)
- `src/plant/models/full/dynamics.py` -> Layer 2 (full model)
- `src/plant/core/physics_matrices.py` -> Layer 2 (physics)
- `src/plant/core/numerical_stability.py` -> Layer 2 (stability)

### Simulation
- `src/simulation/engines/simulation_runner.py` -> Layer 2 (runner)
- `src/simulation/integrators/fixed_step/euler.py` -> Layer 2 (Euler)
- `src/simulation/integrators/fixed_step/runge_kutta.py` -> Layer 2 (RK)
- `src/simulation/integrators/adaptive/runge_kutta.py` -> Layer 2 (adaptive RK)
- `src/simulation/context/safety_guards.py` -> Layer 2 (safety)

### Optimization
- `src/optimization/algorithms/pso_optimizer.py` -> Layer 3 (PSO)
- `src/optimization/algorithms/robust_pso_optimizer.py` -> Layer 3 (robust)
- `src/optimization/core/cost_evaluator.py` -> Layer 3 (costs)
- `src/optimization/validation/enhanced_convergence_analyzer.py` -> Layer 3 (convergence)

### Analysis
- `src/analysis/performance/control_metrics.py` -> Layer 3 (metrics)
- `src/analysis/performance/stability_analysis.py` -> Layer 3 (stability)
- `src/analysis/validation/monte_carlo.py` -> Layer 4 (Monte Carlo)
- `src/analysis/validation/statistical_tests.py` -> Layer 4 (statistics)
- `src/analysis/fault_detection/fdi_system.py` -> Layer 4 (FDI)

### Interfaces & HIL
- `src/interfaces/hil/controller_client.py` -> Layer 4 (HIL client)
- `src/interfaces/hil/plant_server.py` -> Layer 4 (HIL server)
- `src/interfaces/hardware/actuators.py` -> Layer 4 (actuators)
- `src/interfaces/hardware/sensors.py` -> Layer 4 (sensors)

### Infrastructure
- `src/integration/production_readiness.py` -> Layer 4 (production)
- `src/utils/infrastructure/logging/` -> Layer 4 (logging)
- `src/utils/monitoring/realtime/` -> Layer 4 (monitoring)

### Utilities
- `src/utils/control/primitives/saturation.py` -> Layer 2 (primitives)
- `src/utils/visualization/static_plots.py` -> Layer 2 (plotting)
- `src/utils/analysis/chattering.py` -> Layer 3 (chattering)

---

## Learning Strategy Decision Tree

```
Start
  -> Beginner? -> Layer 1 -> Layer 2 -> Layer 3 -> Layer 4 -> Layer 5
  -> Control theory background? -> Layer 2 -> Layer 1 -> Layer 3 -> Layer 4 -> Layer 5
  -> Software engineer? -> Layer 1 -> Layer 2 -> Layer 4 (skip deep theory)
  -> Control engineer? -> Layer 1 -> Layer 2 -> Layer 3 (focus on algorithms)
  -> Deadline-driven project? -> Pick target module -> Learn just-in-time
```

---

## Layer Completion Checks (Short)

- Layer 1: Run 5 simulations, change config parameters, interpret plots
- Layer 2: Explain DIP equations, debug a failed run, choose integrator
- Layer 3: Implement a controller variant, run PSO, compare metrics
- Layer 4: Run Monte Carlo study, validate statistics, deploy HIL
- Layer 5: Add a feature, document it, mentor a contributor

---

**Last Updated:** February 2026
