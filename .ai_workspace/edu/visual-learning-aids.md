# Visual Learning Aids

> ASCII diagrams and flowcharts for layered learning roadmap

**See Full Roadmap:** `.ai_workspace/edu/layered-learning-roadmap.md`

---

## Layer Progression Diagram

```
Layer 1: Foundation (15-20h)
  -> simulate.py, config.yaml, controller interfaces
  -> Outcome: run and modify simulations

Layer 2: Core Mechanics (25-35h)
  -> plant dynamics, simulation engine, integrators
  -> Outcome: understand and debug internals

Layer 3: Advanced Control (35-50h)
  -> SMC variants, PSO optimization, performance analysis
  -> Outcome: design controllers and run experiments

Layer 4: Integration (40-60h)
  -> HIL, statistical validation, production tools
  -> Outcome: deploy and validate at scale

Layer 5: Mastery (50-80h)
  -> architecture, extensibility, research leadership
  -> Outcome: maintain and extend the framework
```

---

## Strategy Comparison (At A Glance)

```
Strategy     Path                       Hours     Best For
TOP-DOWN     1 -> 2 -> 3 -> 4 -> 5       165-245   Beginners
BOTTOM-UP    2 -> 1 -> 3 -> 4 -> 5       140-200   Theorists
ROLE-BASED   Depends on role             75-175    Specialists
PROJECT      Targeted modules only       100-180   Deadlines
```

---

## File Map (Examples)

```
Entry Points
- simulate.py (L1)
- config.yaml (L1)
- streamlit_app.py (L2)

Controllers
- src/controllers/base/controller_interface.py (L1)
- src/controllers/smc/algorithms/super_twisting/ (L3)

Plant & Simulation
- src/plant/models/simplified/dynamics.py (L2)
- src/simulation/engines/simulation_runner.py (L2)
- src/simulation/integrators/fixed_step/runge_kutta.py (L2)

Optimization & Analysis
- src/optimization/algorithms/pso_optimizer.py (L3)
- src/analysis/validation/monte_carlo.py (L4)

Interfaces & Production
- src/interfaces/hil/plant_server.py (L4)
- src/integration/production_readiness.py (L4)
```

---

## Learning Path Flow (Simple)

```
Start -> Layer 1 -> Layer 2
                 -> Layer 3 -> Layer 4 -> Layer 5

Shortcut paths:
- Control theory background: start at Layer 2
- Software engineer: focus on Layer 1, 2, 4
- Control engineer: focus on Layer 1, 2, 3
- Deadline project: pick target module then backfill gaps
```

---

## Layer Completion Checkpoints

```
Layer 1: run 5 sims, edit config, interpret plots
Layer 2: explain equations, debug failures, choose integrator
Layer 3: implement variant, run PSO, compare metrics
Layer 4: Monte Carlo, HIL, production validation
Layer 5: extend framework, document, mentor
```

---

**Last Updated:** February 2026
