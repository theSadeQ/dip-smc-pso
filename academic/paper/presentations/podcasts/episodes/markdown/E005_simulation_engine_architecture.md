# E005: Simulation Engine Architecture

**Part:** Part1 Foundations
**Duration:** 15-20 minutes
**Source:** DIP-SMC-PSO Comprehensive Presentation

---

## Overview

This episode covers simulation engine architecture from the DIP-SMC-PSO project.

## Simulation Architecture Overview

**Core Components:**

        - **SimulationRunner** -- Main orchestration interface
        
            - `src/core/simulation\_runner.py`
            - Coordinates plant, controller, data logging

        - **Unified Simulation Context** -- State management
        
            - `src/core/simulation\_context.py`
            - Thread-safe state updates
            - 3 re-export locations (backward compatibility)

        - **Batch Simulator** -- Numba-accelerated parallel execution
        
            - `src/core/vector\_sim.py`
            - JIT compilation for performance

        - **Integrators** -- Numerical ODE solvers
        
            - RK4, RK45, adaptive schemes
            - `src/core/integrators/`

---

## Simulation Loop: Control Cycle

**Execution Flow (100 Hz control rate):**

    [Visual diagram - see PDF]

---

## Real-Time Simulation Parameters

**Default Configuration:**

    \begin{tabular}{ll}
        \toprule
        **Parameter** & **Value** \\
        \midrule
        Time step ($\Delta t$) & 0.01 s (100 Hz) \\
        Simulation duration & 10 s \\
        Total steps & 1000 \\
        Integrator & RK4 (4th-order Runge-Kutta) \\
        \midrule
        \multicolumn{2}{l}{\textit{Safety Guards:}} \\
        Max angle deviation & $\pm 45^\circ$ \\
        Max cart position & $\pm 2.0$ m \\
        NaN detection & Enabled \\
        \bottomrule
    \end{tabular}

        **Single simulation:** ~10-50 ms (depending on controller complexity) \\
        **100 Monte Carlo runs:** ~5-10 seconds (with Numba acceleration)

---

## Resources

- **Repository:** https://github.com/theSadeQ/dip-smc-pso.git
- **Documentation:** `docs/` directory
- **Getting Started:** `docs/guides/getting-started.md`

---

*Educational podcast episode generated from comprehensive presentation materials*
