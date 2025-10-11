# DIP_SMC_PSO: World-Class Technical Documentation

**Double-Inverted Pendulum Sliding Mode Control with PSO Optimization**

A Python simulation environment for designing, tuning, and analyzing advanced sliding mode controllers for a double-inverted pendulum system. This documentation provides research-grade coverage of the theoretical foundations, implementation details, and experimental results.

## Overview

This project implements multiple sliding mode control strategies for stabilizing a double-inverted pendulum system:

- **Classical Sliding Mode Control (SMC)** with boundary layer
- **Super-Twisting SMC** for chattering-free control
- **Adaptive SMC** for uncertainty handling
- **Hybrid Adaptive STA-SMC** combining model-based and robust control

The controllers are automatically tuned using **Particle Swarm Optimization (PSO)** and validated through simulation and analysis.

## Features

- 🎯 **Multiple Controller Types**: Classical, Super-Twisting, Adaptive, and Hybrid controllers
- 🔧 **Automated Tuning**: PSO-based gain optimization for optimal performance
- 📊 **Analysis**: Lyapunov stability verification and performance metrics
- 🚀 **High Performance**: Numba-accelerated batch simulations
- 🌐 **Dual Interface**: Command-line and Streamlit web interfaces
- 🧪 **Hardware-in-the-Loop**: Real-time simulation features

## Quick Start

```bash
# Basic simulation with classical controller
python simulate.py --ctrl classical_smc --plot

# Optimize and save controller gains
python simulate.py --ctrl sta_smc --run-pso --save tuned_gains.json

# Launch web interface
streamlit run streamlit_app.py
```

## Documentation Structure

```{toctree}
:maxdepth: 2
:caption: 📚 Getting Started

README.md
theory_overview.md
architecture.md
plant_model.md
hil_quickstart.md
streamlit_dashboard_guide.md
```

```{toctree}
:maxdepth: 2
:caption: 📋 Project Documentation

CHANGELOG
CONTRIBUTING
DEPENDENCIES
PATTERNS
context
ACADEMIC_INTEGRITY_STATEMENT
```

```{toctree}
:maxdepth: 2
:caption: 📊 API & Technical Reference

api/index
technical/index
CONTROLLER_FACTORY
controller_pso_interface_api_documentation
factory_integration_documentation
factory_integration_troubleshooting_guide
troubleshooting/index
```

```{toctree}
:maxdepth: 2
:caption: ✅ Testing & Validation Standards

TESTING
validation/index
benchmarks/index
QUICKSTART_VALIDATION
EXAMPLE_VALIDATION_REPORT
control_law_testing_standards
deployment_validation_checklists
benchmarks_methodology
```

```{toctree}
:maxdepth: 2
:caption: 📚 Documentation System

DOCUMENTATION_SYSTEM
DOCUMENTATION_IMPLEMENTATION_PLAN
DOCUMENTATION_STYLE_GUIDE
DOCUMENTATION_COVERAGE_MATRIX
DOCUMENTATION_INVENTORY_SUMMARY
CROSS_REFERENCE_AUDIT_REPORT
```

```{toctree}
:maxdepth: 2
:caption: 🔬 Configuration & Integration

configuration_integration_documentation
configuration_schema_validation
coverage_analysis_methodology
fault_detection_guide
```

## Mathematical Foundation

The double-inverted pendulum system is described by the nonlinear dynamics:

```{math}
:label: eq:dip_dynamics

\vec{M}(\vec{q})\ddot{\vec{q}} + \vec{C}(\vec{q},\dot{\vec{q}})\dot{\vec{q}} + \vec{G}(\vec{q}) = \vec{B}\vec{u}
```

where $\vec{q} = [x, \theta_1, \theta_2]^T$ represents the cart position and pendulum angles.

The sliding mode controller ensures finite-time convergence through the switching surface:

```{math}
:label: eq:sliding_surface

s(\vec{x}) = \vec{S}\vec{x} = \vec{0}
```

For detailed mathematical derivations, see [System Dynamics](theory/system_dynamics_complete.md). The control implementation can be found in the {py:obj}`src.controllers` module.

## Controller Performance Comparison

```{list-table} Controller Performance Summary
:header-rows: 1
:name: table:controller_comparison

* - Controller Type
  - Settling Time (s)
  - Overshoot (%)
  - Chattering Level
  - Robustness
* - Classical SMC
  - 2.1
  - 8.5
  - High
  - Good
* - Super-Twisting SMC
  - 1.8
  - 5.2
  - Low
  - Very Good
* - Adaptive SMC
  - 1.6
  - 4.1
  - Medium
  - Excellent
* - Hybrid Adaptive STA
  - 1.4
  - 3.8
  - Very Low
  - Excellent
```

## PSO Optimization Workflow

The Particle Swarm Optimization process for controller tuning follows this systematic approach:

```{mermaid}
flowchart LR
    Init[Initialize Swarm] --> Eval[Evaluate Fitness J(theta)]
    Eval --> Update[Update p_best & g_best]
    Update --> Velocity[Update Velocity v_i]
    Velocity --> Position[Update Position x_i]
    Position --> Converged{Converged?}
    Converged -- No --> Eval
    Converged -- Yes --> Output[Output theta*]

    subgraph "Fitness Evaluation"
        Eval --> Sim[Run Simulation]
        Sim --> Cost[Calculate Cost Function]
        Cost --> Stability[Check Stability Margins]
    end

    style Init fill:#e1f5fe
    style Output fill:#c8e6c9
    style Converged fill:#fff3e0
```

This optimization process is implemented in {py:obj}`src.optimizer.pso_optimizer.PSOOptimizer` and integrates with all controller types described in {numref}`table:controller_comparison`.

## Bibliography & References

For complete academic citations and attribution, see:

- **{doc}`bibliography`** - Complete BibTeX bibliography with all academic references
- **{doc}`../CITATIONS_ACADEMIC`** - Detailed academic theory citations with exact page numbers
- **{doc}`../DEPENDENCIES`** - Software dependencies and licenses
- **{doc}`../PATTERNS`** - Design patterns and architectural decisions
- **{doc}`../CITATIONS`** - Master citation index and quick reference

### Key References

This project builds upon decades of control theory research. Core references include:

**Sliding Mode Control:**
{cite}`smc_utkin_1992_sliding_modes,smc_slotine_li_1991_applied_nonlinear_control,smc_levant_2003_higher_order_smc`

**PSO Optimization:**
{cite}`pso_kennedy_1995_particle_swarm_optimization,pso_clerc_2002_particle_swarm`

**Stability Theory:**
{cite}`dip_khalil_2002_nonlinear_systems`

For the complete bibliography, see the {doc}`bibliography` page.

## Project Links

- **GitHub Repository**: [github.com/theSadeQ/dip-smc-pso](https://github.com/theSadeQ/dip-smc-pso)
- **Issue Tracker**: [GitHub Issues](https://github.com/theSadeQ/dip-smc-pso/issues)
- **Discussions**: [GitHub Discussions](https://github.com/theSadeQ/dip-smc-pso/discussions)

---

## New Documentation (Phase 6+)

### Getting Started & Tutorials

- **[📘 Interactive Jupyter Notebook](../notebooks/01_getting_started.ipynb)** (NEW)
  - 30-45 minute interactive tutorial
  - All 4 controllers with comparisons
  - PSO optimization walkthrough
  - Phase portraits and energy analysis

### Deployment & Production

- **[🐳 Docker Deployment Guide](deployment/docker.md)** (NEW)
  - Quick start with pre-built images
  - Multi-stage build optimization (2GB → 400MB)
  - Docker Compose for HIL
  - GPU support and cloud deployment (AWS/GCP/Azure/K8s)
  - Troubleshooting

### Advanced Topics

- **[🔬 Numerical Stability Guide](advanced/numerical_stability.md)** (NEW)
  - Matrix conditioning and regularization
  - Adaptive parameter tuning
  - Error analysis (truncation, round-off, Lyapunov)
  - Implementation patterns and testing
  - Essential for production deployments

### Research & Workflow

- **[📊 Research Workflow Guide](workflow/research_workflow.md)** (NEW)
  - Complete lifecycle: hypothesis → publication
  - 7-phase workflow with examples
  - Statistical analysis and visualization
  - Reproducibility checklist
  - Publication preparation

### Contributing

- **[📝 Contributing Guide](../CONTRIBUTING.md)** (UPDATED)
  - Development workflow with branch strategy
  - Code standards (PEP 8, type hints ≥95%)
  - Conventional commits format
  - Pull request templates
  - Quality gates and testing requirements

---

## Complete Documentation Structure

```{toctree}
:maxdepth: 2
:caption: 📚 User Guides & Tutorials

guides/index
tutorials/index
workflows/index
```

```{toctree}
:maxdepth: 2
:caption: 📊 Analysis & Reports

analysis/index
reports/index
```

```{toctree}
:maxdepth: 2
:caption: 🗺️ Project Planning & Roadmaps

plans/index
```

```{toctree}
:maxdepth: 2
:caption: 🚀 Production & Deployment

production/index
deployment/DEPLOYMENT_GUIDE
```

```{toctree}
:maxdepth: 2
:caption: 📽️ Presentation Materials

presentation/index
```

```{toctree}
:maxdepth: 2
:caption: 🔬 Mathematical Foundations

mathematical_foundations/index
theory/index
```

```{toctree}
:maxdepth: 2
:caption: 🏭 Controller Factory & Integration

factory/README
controllers/index
```

```{toctree}
:maxdepth: 2
:caption: 🧪 Testing & Quality Assurance

testing/index
TESTING
```

```{toctree}
:maxdepth: 2
:caption: 🔧 MCP Debugging & Code Quality

mcp-debugging/index
```

```{toctree}
:maxdepth: 2
:caption: 📖 References & Bibliography

bibliography
references/index
CITATIONS
CITATIONS_ACADEMIC
```

