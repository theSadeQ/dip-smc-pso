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

ACADEMIC_INTEGRITY_STATEMENT
CHANGELOG
CITATIONS
CITATIONS_ACADEMIC
CITATION_SYSTEM
CITATION_SYSTEM_IMPLEMENTATION
CODE_BEAUTIFICATION_SPECIALIST_COMPREHENSIVE_ASSESSMENT
CONTRIBUTING
CONTROLLER_FACTORY
CROSS_REFERENCE_AUDIT_REPORT
DEPENDENCIES
DOCUMENTATION_COVERAGE_MATRIX
DOCUMENTATION_IMPLEMENTATION_PLAN
DOCUMENTATION_INVENTORY_SUMMARY
DOCUMENTATION_STYLE_GUIDE
DOCUMENTATION_SYSTEM
EXAMPLE_VALIDATION_REPORT
GITHUB_ISSUE_9_ULTIMATE_ORCHESTRATOR_STRATEGIC_PLAN
IMPLEMENTATION_REPORT
LICENSES
PACKAGE_CONTENTS
PATTERNS
PHASE6_COMPLETION_SUMMARY
PHASE_3_1_COMPLETION_REPORT
PLANT_CONFIGURATION
PSO_Documentation_Validation_Report
PSO_INTEGRATION_GUIDE
QUICKSTART_VALIDATION
README
RELEASE_CHECKLIST
SPHINX_100_PERCENT_COMPLETION_REPORT
SPHINX_PHASE10_COMPLETION_REPORT
SPHINX_PHASE11_COMPLETION_REPORT
SPHINX_PHASE2_COMPLETION_REPORT
SPHINX_PHASE3_COMPLETION_REPORT
SPHINX_PHASE4_COMPLETION_REPORT
SPHINX_PHASE5_COMPLETION_REPORT
SPHINX_PHASE6_COMPLETION_REPORT
SPHINX_PHASE8_SUMMARY
SPHINX_PHASE9_PROGRESS_REPORT
TESTING
ULTIMATE_ORCHESTRATOR_EXECUTIVE_DEPLOYMENT_SUMMARY
analysis_plan
api/index
architecture
architecture_control_room
ast_traversal_patterns
benchmarks/index
benchmarks_methodology
bibliography
changelog
cheat-sheet-template
citation_faq
citation_quick_reference
claim_extraction_guide
claude-backup
component-index-template
configuration-reference
configuration_integration_documentation
configuration_schema_validation
context
control_law_testing_standards
controller_pso_interface_api_documentation
coverage_analysis_methodology
deployment/DEPLOYMENT_GUIDE
deployment/STREAMLIT_DEPLOYMENT
deployment/docker
deployment_validation_checklists
documentation_structure
executive_summary_template
fault_detection_guide
fault_detection_system_documentation
fdi_threshold_calibration_methodology
guides/getting-started
guides/getting-started-validation-report
guides/index
hil_quickstart
integration-guide
integration-guide-template
maintenance-guide
mathematical_algorithm_validation
mathematical_foundations/index
mathematical_validation_procedures
memory_management_patterns
memory_management_quick_reference
module-readme-template
numerical_stability_guide
plant_model
production/index
pso_configuration_schema_documentation
pso_convergence_plots
pso_convergence_theory
pso_factory_integration_patterns
pso_integration_technical_specification
pso_optimization_workflow_specifications
pso_optimization_workflow_user_guide
pso_troubleshooting_maintenance_manual
quality_gate_independence_framework
quality_gates
quick-start-template
reference/analysis/index
reference/controllers/index
reference/interfaces/index
reference/optimization/index
reference/plant/index
reference/simulation/index
reference/utils/index
regex_pattern_reference
reproduction_guide
research_workflow
results_readme
safe_operations_reference
safety_system_validation_protocols
sitemap_cards
sitemap_interactive
sitemap_visual
streamlit_dashboard_guide
symbols
technical-reference
test_execution_execution_guide
test_execution_guide
test_infrastructure_documentation
test_infrastructure_validation_report
test_protocols
testing-and-benchmarks
testing/index
theorem_verification_guide
theory/index
theory_overview
use_cases
validation/index
verification_checklist
versioning_guide
workflows/index
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
