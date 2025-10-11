# Documentation Structure & Site Map

This page provides a complete overview of the DIP_SMC_PSO documentation organization. Use this as a roadmap to navigate through technical references, user guides, tutorials, and research documentation.

## Overview

The documentation is organized into several main categories:

- **Getting Started**: Installation guides, quickstart tutorials, and basic concepts
- **User Guides & Tutorials**: Step-by-step instructions for common tasks and workflows
- **API & Technical Reference**: Detailed API documentation and module references
- **Testing & Validation**: Testing standards, benchmarking methodologies, and quality assurance
- **Production & Deployment**: Deployment guides, Docker setup, and production readiness
- **Research & Analysis**: Research workflows, data analysis, and publication preparation
- **Project Documentation**: Changelog, contributing guidelines, design patterns

---

## Getting Started

Essential documentation for new users to get up and running quickly.

```{toctree}
:maxdepth: 2
:caption: Getting Started

README.md
theory_overview.md
architecture.md
plant_model.md
hil_quickstart.md
streamlit_dashboard_guide.md
guides/getting-started
```

---

## User Guides & Tutorials

Step-by-step tutorials and how-to guides for common tasks and workflows.

```{toctree}
:maxdepth: 2
:caption: User Guides & Tutorials

guides/index
tutorials/index
workflows/index
```

**Key Resources:**
- Interactive tutorials for first simulations
- Controller comparison guides
- PSO optimization workflows
- Custom controller development

---

## API & Technical Reference

Comprehensive technical reference for all modules, classes, and functions.

```{toctree}
:maxdepth: 2
:caption: API & Technical Reference

api/index
technical/index
CONTROLLER_FACTORY
controller_pso_interface_api_documentation
factory_integration_documentation
factory_integration_troubleshooting_guide
troubleshooting/index
references/index
```

**Detailed References:**
- {doc}`reference/controllers/index` - Controller implementations
- {doc}`reference/optimization/index` - PSO optimization modules
- {doc}`reference/simulation/index` - Simulation engines
- {doc}`reference/plant/index` - Dynamics models
- {doc}`reference/analysis/index` - Analysis and metrics
- {doc}`reference/utils/index` - Utility functions

---

## Testing & Validation Standards

Testing methodologies, validation protocols, and quality assurance frameworks.

```{toctree}
:maxdepth: 2
:caption: Testing & Validation

TESTING
validation/index
benchmarks/index
testing/index
QUICKSTART_VALIDATION
EXAMPLE_VALIDATION_REPORT
control_law_testing_standards
deployment_validation_checklists
benchmarks_methodology
```

**Testing Coverage:**
- Unit tests for all controllers
- Integration tests for simulation workflows
- Benchmark tests for performance validation
- Statistical validation protocols

---

## Production & Deployment

Guides for deploying the framework in production environments.

```{toctree}
:maxdepth: 2
:caption: Production & Deployment

production/index
deployment/DEPLOYMENT_GUIDE
deployment/docker
deployment/STREAMLIT_DEPLOYMENT
```

**Deployment Options:**
- Docker containerization
- Streamlit dashboard deployment
- Cloud deployment (AWS, GCP, Azure)
- Kubernetes orchestration
- Production readiness checklist

---

## Mathematical Foundations

Theoretical foundations, mathematical derivations, and algorithm analysis.

```{toctree}
:maxdepth: 2
:caption: Mathematical Foundations

mathematical_foundations/index
theory/index
```

**Theory Coverage:**
- Sliding mode control theory
- PSO algorithm foundations
- Lyapunov stability analysis
- Double inverted pendulum dynamics
- Finite-time convergence proofs

---

## Controller Factory & Integration

Documentation for the controller factory system and integration patterns.

```{toctree}
:maxdepth: 2
:caption: Controller Factory & Integration

factory/README
controllers/index
```

**Factory System:**
- Controller registration and discovery
- PSO integration patterns
- Parameter interface specification
- Performance benchmarks
- Migration guides

---

## Analysis & Reports

Performance analysis, experimental reports, and research findings.

```{toctree}
:maxdepth: 2
:caption: Analysis & Reports

analysis/index
reports/index
```

**Analysis Tools:**
- Controller performance comparison
- PSO convergence analysis
- Statistical benchmarking
- Fault detection reports
- Memory pattern analysis

---

## Project Planning & Roadmaps

Project plans, roadmaps, and development documentation.

```{toctree}
:maxdepth: 2
:caption: Project Planning

plans/index
```

---

## Project Documentation

Project-level documentation including changelog, contributing guidelines, and design patterns.

```{toctree}
:maxdepth: 2
:caption: Project Documentation

CHANGELOG
CONTRIBUTING
DEPENDENCIES
PATTERNS
context
ACADEMIC_INTEGRITY_STATEMENT
```

---

## Configuration & Integration

Configuration schemas, validation, and system integration documentation.

```{toctree}
:maxdepth: 2
:caption: Configuration

configuration_integration_documentation
configuration_schema_validation
coverage_analysis_methodology
fault_detection_guide
```

---

## Documentation System

Meta-documentation about the documentation system itself.

```{toctree}
:maxdepth: 2
:caption: Documentation System

DOCUMENTATION_SYSTEM
DOCUMENTATION_IMPLEMENTATION_PLAN
DOCUMENTATION_STYLE_GUIDE
DOCUMENTATION_COVERAGE_MATRIX
DOCUMENTATION_INVENTORY_SUMMARY
CROSS_REFERENCE_AUDIT_REPORT
```

---

## MCP Debugging & Code Quality

MCP server debugging workflows and code quality tools.

```{toctree}
:maxdepth: 2
:caption: MCP Debugging

mcp-debugging/index
```

---

## Presentation Materials

Slides, diagrams, and visual materials for presentations and teaching.

```{toctree}
:maxdepth: 2
:caption: Presentation Materials

presentation/index
```

---

## References & Bibliography

Academic references, citations, and bibliographic information.

```{toctree}
:maxdepth: 2
:caption: References & Bibliography

bibliography
CITATIONS
CITATIONS_ACADEMIC
```

**Citation Management:**
- Complete BibTeX bibliography
- Detailed page-numbered citations
- Software dependencies and licenses
- Design pattern attributions

---

## Quick Navigation

**Most Common Pages:**

- [Getting Started Guide](guides/getting-started.md) - Begin here
- [API Index](api/index.md) - Complete API reference
- [Controller Factory](factory/README.md) - Controller system architecture
- [PSO Optimization](api/pso_optimization.md) - Optimization workflows
- [Testing Guide](TESTING.md) - Test execution and standards
- [Contributing](CONTRIBUTING.md) - Development guidelines

**Frequently Accessed:**

- [Troubleshooting](troubleshooting/index.md) - Common issues and solutions
- [Deployment Guide](deployment/DEPLOYMENT_GUIDE.md) - Production deployment
- [Docker Setup](deployment/docker.md) - Containerization
- [Benchmarks](benchmarks/index.md) - Performance benchmarks

---

## Search & Discovery

**Finding What You Need:**

1. **By Task**: Use the [User Guides](guides/index.md) for task-oriented instructions
2. **By Module**: Use the [API Reference](api/index.md) for code documentation
3. **By Topic**: Use the [Theory Overview](theory/index.md) for conceptual understanding
4. **By Example**: Use the [Tutorials](tutorials/index.md) for hands-on learning

**Search Tips:**

- Use the search bar (top-right) for full-text search
- Browse by category using the sidebar navigation
- Check cross-references for related topics
- Refer to the bibliography for academic citations

---

**Last Updated:** 2025-10-11
