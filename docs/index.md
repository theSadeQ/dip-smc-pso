# DIP SMC PSO Documentation

**Advanced Control System for Double-Inverted Pendulum**

Welcome to the documentation for the DIP SMC PSO framework - a research-grade Python environment for designing, tuning, and analyzing sliding mode controllers for highly unstable nonlinear systems.

## Overview

This framework implements state-of-the-art sliding mode control strategies with automated parameter tuning through Particle Swarm Optimization. The system targets the double-inverted pendulum (DIP) - a benchmark problem in nonlinear control theory requiring simultaneous stabilization of two coupled pendulums on a movable cart.

**Key Capabilities:**
- **Research-Grade Implementation**: Validated against published control theory with complete mathematical derivations
- **Multiple Controller Architectures**: Classical SMC, Super-Twisting Algorithm, Adaptive SMC, and Hybrid Adaptive STA-SMC
- **Intelligent Optimization**: Automated controller gain tuning using PSO with convergence guarantees
- **Production-Ready Deployment**: Docker containers, CI/CD pipelines, and comprehensive test coverage (>85%)
- **Hardware-in-the-Loop Support**: Real-time simulation interface for physical system integration
- **Extensible Architecture**: Plugin-based controller factory with type-safe parameter interfaces

## Features

**Control Algorithms**
- Classical Sliding Mode Control with boundary layer for chattering reduction
- Super-Twisting Algorithm for finite-time convergence without chattering
- Adaptive SMC with online uncertainty estimation
- Hybrid Adaptive STA-SMC combining model-based and robust control

**Optimization & Tuning**
- Particle Swarm Optimization with configurable swarm dynamics
- Multi-objective cost functions (stability, performance, robustness)
- Convergence analysis and parameter sensitivity tools
- Automated bounds validation and constraint handling

**Analysis & Validation**
- Lyapunov stability verification with numerical certificates
- Statistical benchmarking with confidence intervals
- Monte Carlo robustness analysis
- Fault detection and isolation framework

**Development & Deployment**
- Type-safe configuration with Pydantic schemas
- Numba-accelerated batch simulations for parameter sweeps
- Streamlit interactive dashboard for real-time visualization
- Docker deployment with GPU support for cloud platforms

**Documentation Features**
- **NEW: Progressive Web App** - Install as native app, full offline documentation access, automatic updates, works without internet
- **NEW: 3D Interactive Pendulum** - Real-time WebGL physics simulation with adjustable parameters (world's first in technical docs!)
- **NEW: Live Python Code Execution** - Run Python+NumPy+Matplotlib directly in browser, edit and execute examples instantly, zero installation required
- Collapsible code blocks with state persistence for improved readability
- Interactive visualizations and performance dashboards
- GPU-accelerated smooth animations (60 FPS)
- Full accessibility support with keyboard navigation

## Main Commands

```bash
# Run simulation with specific controller
python simulate.py --ctrl classical_smc --plot
python simulate.py --ctrl sta_smc --plot
python simulate.py --ctrl adaptive_smc --plot
python simulate.py --ctrl hybrid_adaptive_sta_smc --plot

# Optimize controller gains with PSO
python simulate.py --ctrl classical_smc --run-pso --save gains_classical.json
python simulate.py --ctrl sta_smc --run-pso --save gains_sta.json

# Load optimized gains and run
python simulate.py --load tuned_gains.json --plot

# Launch interactive web dashboard
streamlit run streamlit_app.py

# Run hardware-in-the-loop simulation
python simulate.py --run-hil --plot

# Run test suite
pytest tests/ -v
pytest tests/test_controllers/ --benchmark-only

# Build documentation
cd docs && sphinx-build -b html . _build/html
python -m http.server 8000 --directory docs/_build/html
```

```{toctree}
:maxdepth: 3
:hidden:

README
guides/getting-started
guides/getting-started-validation-report
streamlit_dashboard_guide
hil_quickstart

architecture_control_room
sitemap_interactive
sitemap_cards
sitemap_visual
documentation_structure

guides/index
workflows/index

api/index
reference/controllers/index
reference/optimization/index
reference/simulation/index
reference/plant/index
reference/analysis/index
reference/utils/index
reference/interfaces/index

theory/index
theory/pso_algorithm_foundations
mathematical_foundations/index
plant_model
architecture
theory_overview

TESTING
testing/index
benchmarks/index
validation/index
test_infrastructure_validation_report
test_execution_guide
QUICKSTART_VALIDATION

deployment/DEPLOYMENT_GUIDE
deployment/docker
deployment/STREAMLIT_DEPLOYMENT
production/index

CHANGELOG
CONTRIBUTING
DEPENDENCIES
PATTERNS
CITATIONS
bibliography
context
```

## Visual Navigation

**Explore the documentation your way:**

::::{grid} 1 2 3 3
:gutter: 3

:::{grid-item-card} 🎮 3D Interactive Pendulum (NEW!)
:link: guides/interactive/3d-pendulum-demo
:link-type: doc

Real-time physics simulation with WebGL rendering - adjust gains, set angles, watch dynamics unfold in cinematic 3D
:::

:::{grid-item-card} 🐍 Live Python Code (NEW!)
:link: guides/interactive/live-python-demo
:link-type: doc

Run Python code in browser with NumPy, Matplotlib - edit examples, see results instantly, zero installation
:::

:::{grid-item-card} 📱 Install as App (NEW!)
:link: SPHINX_PHASE6_COMPLETION_REPORT
:link-type: doc

Progressive Web App - Install on mobile/desktop, work offline, automatic updates, native app experience
:::

:::{grid-item-card} 🎛️ Control Room
:link: architecture_control_room
:link-type: doc

Isometric 3D system architecture with interactive components
:::

:::{grid-item-card} 🎯 Interactive Graph
:link: sitemap_interactive
:link-type: doc

Click, drag, and zoom through an interactive force-directed visualization
:::

:::{grid-item-card} 🎨 Card View
:link: sitemap_cards
:link-type: doc

Beautiful card-based navigation with icons and descriptions
:::

:::{grid-item-card} 🗺️ Mindmap
:link: sitemap_visual
:link-type: doc

Mermaid mindmap and flowchart visualizations
:::

:::{grid-item-card} 📜 Text Sitemap
:link: documentation_structure
:link-type: doc

Traditional hierarchical text-based sitemap
:::

::::

## Quick Start

### First Simulation (5 minutes)
```bash
# Install dependencies
pip install -r requirements.txt

# Run your first simulation
python simulate.py --ctrl classical_smc --plot

# Launch interactive dashboard
streamlit run streamlit_app.py
```

### Optimize Controller Gains (15 minutes)
```bash
# Run PSO optimization
python simulate.py --ctrl adaptive_smc --run-pso --save gains_adaptive.json

# Test optimized controller
python simulate.py --load gains_adaptive.json --plot
```

### Run Test Suite
```bash
pytest tests/ -v
pytest tests/test_controllers/ --benchmark-only
```

## Key Documentation Pages

**New Users**
- {doc}`guides/getting-started` - Complete installation and first simulation guide
- {doc}`streamlit_dashboard_guide` - Interactive web dashboard tutorial
- {doc}`guides/how-to/running-simulations` - Simulation workflows and best practices

**Developers**
- {doc}`api/index` - Complete API reference
- {doc}`CONTRIBUTING` - Development guidelines and PR workflow
- {doc}`TESTING` - Test execution and coverage standards

**Researchers**
- {doc}`theory/pso_algorithm_foundations` - Mathematical foundations of PSO
- {doc}`benchmarks/index` - Controller performance benchmarks
- {doc}`bibliography` - Academic references and citations

## Project Information

- **GitHub**: [github.com/theSadeQ/dip-smc-pso](https://github.com/theSadeQ/dip-smc-pso)
- **Issues**: [github.com/theSadeQ/dip-smc-pso/issues](https://github.com/theSadeQ/dip-smc-pso/issues)
- **License**: See {doc}`DEPENDENCIES` for software licenses and attributions
- **Citations**: See {doc}`CITATIONS` for academic references and {doc}`bibliography` for complete BibTeX

---

**Last Updated**: October 2025
**Version**: 1.0.0
**Status**: Production Ready
