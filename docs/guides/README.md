# User Guides & Tutorials

Welcome to the DIP SMC PSO framework documentation! This guide will help you navigate the documentation and find what you need.

---

## Quick Navigation

### 🚀 Getting Started
**Start here if you're new to the framework**

- [**Getting Started Guide**](getting-started.md)
  Complete setup and first simulation in 10 minutes

### 📘 User Guide
**Comprehensive reference for daily usage**

- [**User Guide**](user-guide.md)
  Core workflows, configuration, PSO optimization, result analysis

### 📚 Tutorial Series
**Step-by-step learning path**

1. [**Tutorial 01: Your First Simulation**](tutorials/tutorial-01-first-simulation.md)
   Learn DIP system, run classical SMC, interpret results (30-45 min)

2. [**Tutorial 02: Controller Comparison**](tutorials/tutorial-02-controller-comparison.md)
   Compare 4 core SMC controllers, understand tradeoffs, select optimal controller (45-60 min)

3. [**Tutorial 03: PSO Optimization**](tutorials/tutorial-03-pso-optimization.md)
   Automatic gain tuning, convergence analysis, custom cost functions (60-90 min)

4. [**Tutorial 04: Custom Controller Development**](tutorials/tutorial-04-custom-controller.md)
   Implement Terminal SMC from scratch, factory integration, testing (90-120 min)

5. [**Tutorial 05: Research Workflow**](tutorials/tutorial-05-research-workflow.md)
   End-to-end research project, statistical analysis, publication workflow (120+ min)

---

## Documentation Structure

```
docs/guides/
├── README.md                          # This file (navigation)
├── getting-started.md                 # Quick setup (523 lines)
├── user-guide.md                      # Comprehensive reference (826 lines)
├── QUICK_REFERENCE.md                 # Command cheat sheet
└── tutorials/                         # Tutorial series
    ├── tutorial-01-first-simulation.md         (600 lines)
    ├── tutorial-02-controller-comparison.md    (797 lines)
    ├── tutorial-03-pso-optimization.md         (865 lines)
    ├── tutorial-04-custom-controller.md        (784 lines)
    └── tutorial-05-research-workflow.md        (640 lines)
```

**Total: 5,035 lines of user documentation**

---

## Learning Paths

### Path 1: Quick Start (1-2 hours)
Perfect for: First-time users, quick prototyping

1. [Getting Started](getting-started.md) → Install & run first simulation
2. [Tutorial 01](tutorials/tutorial-01-first-simulation.md) → Understand DIP & SMC basics
3. [User Guide - Running Simulations](user-guide.md#running-simulations) → Explore CLI options

### Path 2: Controller Expert (4-6 hours)
Perfect for: Control systems researchers, comparative studies

1. [Getting Started](getting-started.md) → Setup
2. [Tutorial 01](tutorials/tutorial-01-first-simulation.md) → Basics
3. [Tutorial 02](tutorials/tutorial-02-controller-comparison.md) → Compare controllers
4. [Tutorial 03](tutorials/tutorial-03-pso-optimization.md) → Optimize gains
5. [User Guide - PSO Optimization](user-guide.md#pso-optimization) → Advanced tuning

### Path 3: Custom Development (8-12 hours)
Perfect for: Implementing novel SMC algorithms

1. [Getting Started](getting-started.md) → Setup
2. [Tutorial 01-02](tutorials/) → Learn framework basics
3. [Tutorial 04](tutorials/tutorial-04-custom-controller.md) → Implement custom controller
4. [Tutorial 03](tutorials/tutorial-03-pso-optimization.md) → Optimize custom controller
5. [User Guide - Configuration](user-guide.md#configuration-management) → Advanced config

### Path 4: Research Publication (12+ hours)
Perfect for: Graduate students, researchers

1. Complete Paths 1-2 (understand framework & controllers)
2. [Tutorial 05](tutorials/tutorial-05-research-workflow.md) → End-to-end research project
3. [User Guide - Batch Processing](user-guide.md#batch-processing) → Monte Carlo studies
4. [User Guide - Result Analysis](user-guide.md#result-analysis) → Statistical validation

---

## Quick Reference

### Most Common Commands

```bash
# Run simulation
python simulate.py --ctrl classical_smc --plot

# Optimize gains
python simulate.py --ctrl classical_smc --run-pso --save gains.json

# Test optimized gains
python simulate.py --load gains.json --plot

# Web interface
streamlit run streamlit_app.py

# Run tests
python run_tests.py
```

See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for full command reference.

---

## Controllers Overview

| Controller | Best For | Computational Cost | Chattering |
|------------|----------|-------------------|------------|
| **Classical SMC** | Prototyping, known systems | Low | Moderate |
| **Super-Twisting SMC** | Chattering-sensitive apps | Medium | None |
| **Adaptive SMC** | Uncertain/varying systems | Medium-High | Low |
| **Hybrid Adaptive STA** | High-performance control | High | None |

**Decision Tree:**
- Need smooth control? → Super-Twisting or Hybrid
- Parameter uncertainty? → Adaptive or Hybrid
- Simplicity priority? → Classical
- Best overall? → Hybrid Adaptive STA

---

## Key Concepts

### System
- **DIP (Double-Inverted Pendulum):** Two pendulums on a cart, 6-state system
- **Underactuated:** 3 DOF, 1 control input (cart force)
- **Unstable equilibrium:** Both pendulums vertical

### Control
- **SMC (Sliding Mode Control):** Nonlinear control with sliding surface
- **Sliding Surface:** `s = k₁θ₁ + k₂dθ₁ + λ₁θ₂ + λ₂dθ₂`
- **Chattering:** High-frequency oscillations from discontinuous switching

### Optimization
- **PSO (Particle Swarm Optimization):** Bio-inspired algorithm for gain tuning
- **Swarm:** Collection of candidate solutions (particles)
- **Convergence:** Process of finding optimal gains (typically 50-100 iterations)

### Metrics
- **ISE:** Integral Squared Error (tracking accuracy)
- **ITAE:** Integral Time-Absolute Error (convergence speed)
- **Settling Time:** Time to reach ±5% of setpoint
- **Overshoot:** Peak deviation beyond setpoint

---

## Troubleshooting

### Simulation Won't Run
1. Check Python version: `python --version` (need ≥3.9)
2. Verify installation: `pip list | findstr numpy`
3. Check working directory: Must be project root

### PSO Not Converging
1. Increase iterations: `--override "pso.iters=200"`
2. Widen bounds in `config.yaml`
3. Try different random seed: `--seed 123`

### Performance Issues
1. Use simplified dynamics: `--override "use_full_dynamics=false"`
2. Reduce simulation duration: `--override "simulation.duration=3.0"`
3. Increase timestep: `--override "simulation.dt=0.02"` (test stability)

See [User Guide - Troubleshooting](user-guide.md#troubleshooting) for complete guide.

---

## Contributing

Found an issue or have a suggestion?
- Open an issue: https://github.com/theSadeQ/dip-smc-pso/issues
- Discuss improvements in [User Guide](user-guide.md)

---

## License & Citation

This framework is open-source. If you use it in research, please cite:

```bibtex
@software{dip_smc_pso_2025,
  title={DIP SMC PSO: Double-Inverted Pendulum Sliding Mode Control with PSO Optimization},
  author={...},
  year={2025},
  url={https://github.com/theSadeQ/dip-smc-pso}
}
```

---

**Happy Experimenting!** 🚀

For questions, consult the [User Guide](user-guide.md) or open an issue on GitHub.
