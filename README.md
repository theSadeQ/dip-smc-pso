# Double-Inverted Pendulum Sliding Mode Control with PSO Optimization

[![Build Status](https://github.com/theSadeQ/dip-smc-pso/workflows/CI/badge.svg)](https://github.com/theSadeQ/dip-smc-pso/actions)
[![Documentation](https://readthedocs.org/projects/dip-smc-pso/badge/?version=latest)](https://dip-smc-pso.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A comprehensive Python framework for simulating, controlling, and analyzing a double-inverted pendulum (DIP) system using advanced sliding mode control (SMC) techniques with Particle Swarm Optimization (PSO). This project provides a complete ecosystem for control systems research, education, and industrial applications.

## Key Features

### Advanced Control Systems
- **Multiple SMC Variants**: Classical SMC, Super-Twisting (STA), Adaptive SMC, Hybrid Adaptive STA-SMC
- **Model Predictive Control (MPC)**: Experimental MPC implementation with constraint handling
- **Swing-Up Controllers**: Specialized controllers for large-angle stabilization
- **Controller Factory**: Extensible factory pattern for easy controller instantiation

### Intelligent Optimization
- **PSO Optimization**: Multi-objective particle swarm optimization for gain tuning
- **Convergence Analysis**: Advanced convergence detection and validation
- **Parameter Bounds**: Intelligent constraint handling for realistic control parameters
- **Multi-Algorithm Support**: Framework for additional optimization algorithms

### Plant Models & Dynamics
- **Simplified Dynamics**: Fast linearized model for rapid prototyping
- **Full Nonlinear Model**: High-fidelity dynamics with coupling effects
- **Low-Rank Approximation**: Computationally efficient reduced-order model
- **Numerical Stability**: Robust handling of ill-conditioned dynamics

### High-Performance Simulation
- **Vectorized Batch Simulation**: Numba-accelerated parallel execution
- **Multiple Integrators**: Adaptive and fixed-step integration schemes
- **Safety Guards**: Comprehensive constraint monitoring and violation detection
- **Real-Time Capabilities**: Hardware-in-the-loop (HIL) simulation support

### Analysis & Visualization
- **Fault Detection**: Advanced FDI (Fault Detection and Isolation) system
- **Performance Metrics**: Lyapunov stability, settling time, overshoot analysis
- **Statistical Validation**: Monte Carlo analysis, confidence intervals
- **Interactive Dashboards**: Real-time plotting and parameter adjustment

### Development & Production
- **Comprehensive Testing**: Unit, integration, property-based, and benchmark tests
- **Type Safety**: Full type hint coverage with mypy validation
- **Configuration Management**: YAML-based configuration with validation
- **Documentation**: Complete Sphinx documentation with examples

## Architecture Overview

```
DIP SMC PSO Framework
├── Controllers/           # Control algorithms and factory
│   ├── SMC Variants       # Classical, STA, Adaptive, Hybrid
│   ├── MPC Controller     # Model Predictive Control
│   └── Specialized        # Swing-up and custom controllers
├── Plant Models/          # System dynamics
│   ├── Simplified         # Linearized for fast iteration
│   ├── Full Nonlinear     # High-fidelity physics
│   └── Low-Rank           # Efficient approximation
├── Core Engine/           # Simulation infrastructure
│   ├── Simulation Runner  # Main execution engine
│   ├── Vector Simulation  # Batch/parallel processing
│   └── Safety Guards      # Constraint monitoring
├── Optimization/          # Parameter tuning
│   ├── PSO Algorithm      # Particle swarm optimization
│   ├── Objectives         # Multi-objective cost functions
│   └── Convergence        # Analysis and validation
├── Analysis/              # Performance evaluation
│   ├── Fault Detection    # FDI system
│   ├── Statistics         # Monte Carlo, confidence intervals
│   └── Visualization      # Plots and animations
├── Interfaces/            # External connectivity
│   ├── HIL Support        # Hardware-in-the-loop
│   ├── Network Protocols  # UDP, TCP, WebSocket
│   └── Data Exchange      # Serialization and streaming
└── Utils/                 # Supporting tools
    ├── Configuration      # YAML validation
    ├── Monitoring         # Performance tracking
    └── Development        # Testing and debugging
```

## Quick Start

### Prerequisites
- **Python 3.9+** (recommended: 3.11)
- **Git** for version control
- **Optional**: CUDA-capable GPU for accelerated simulations

### Installation

```bash
# Clone the repository
git clone https://github.com/theSadeQ/dip-smc-pso.git
cd dip-smc-pso

# Install dependencies
pip install -r requirements.txt

# Verify installation
python simulate.py --help
```

### First Simulation

```bash
# Run a basic classical SMC simulation
python simulate.py --ctrl classical_smc --plot

# Launch the interactive web interface
streamlit run streamlit_app.py
```

## Usage Guide

### Command-Line Interface (CLI)

#### Basic Simulations
```bash
# Classical SMC with plotting
python simulate.py --ctrl classical_smc --plot

# Super-Twisting SMC with full dynamics
python simulate.py --ctrl sta_smc --dynamics full --plot

# Adaptive SMC with disturbances
python simulate.py --ctrl adaptive_smc --disturbance --plot
```

#### PSO Optimization
```bash
# Optimize classical SMC gains
python simulate.py --ctrl classical_smc --run-pso --save gains_classical.json

# Optimize with custom parameters
python simulate.py --ctrl sta_smc --run-pso --particles 50 --generations 100

# Load pre-optimized gains
python simulate.py --load gains_classical.json --plot
```

#### Hardware-in-the-Loop (HIL)
```bash
# Start HIL plant server
python simulate.py --run-hil-server --port 8888

# Run HIL controller client
python simulate.py --run-hil --host localhost --port 8888
```

#### Batch Analysis
```bash
# Monte Carlo analysis
python simulate.py --ctrl classical_smc --monte-carlo --runs 1000

# Statistical validation
python simulate.py --ctrl sta_smc --statistical-analysis
```

### Interactive Web Application

Launch the Streamlit dashboard for real-time interaction:

```bash
streamlit run streamlit_app.py
```

**Features:**
- Real-time parameter tuning
- Live performance metrics
- Animation visualization
- Comparative analysis
- Configuration export/import

### Configuration Management

```bash
# Use custom configuration
python simulate.py --config custom_config.yaml

# Print current configuration
python simulate.py --print-config

# Validate configuration
python simulate.py --validate-config
```

## Project Structure

```
dip-smc-pso/
├── simulate.py              # Main CLI application
├── streamlit_app.py         # Web dashboard
├── config.yaml              # Main configuration
├── requirements.txt         # Python dependencies
├── src/                     # Source code
│   ├── controllers/         # Control algorithms
│   │   ├── smc/             # SMC implementations
│   │   ├── mpc/             # Model predictive control
│   │   ├── specialized/     # Custom controllers
│   │   └── factory.py       # Controller factory
│   ├── plant/               # Plant models
│   │   ├── models/          # Dynamics implementations
│   │   └── configurations/  # Model parameters
│   ├── core/                # Simulation engine
│   │   ├── simulation_runner.py
│   │   ├── vector_sim.py    # Batch simulation
│   │   └── safety_guards.py
│   ├── optimization/        # Parameter optimization
│   │   ├── algorithms/      # PSO and others
│   │   ├── objectives/      # Cost functions
│   │   └── results/         # Analysis tools
│   ├── analysis/            # Performance analysis
│   │   ├── fault_detection/ # FDI system
│   │   ├── validation/      # Statistical tests
│   │   └── visualization/   # Plotting tools
│   ├── interfaces/          # External interfaces
│   │   ├── hil/            # Hardware-in-the-loop
│   │   ├── network/        # Communication protocols
│   │   └── monitoring/     # Performance monitoring
│   └── utils/               # Utilities
│       ├── validation/      # Parameter validation
│       ├── reproducibility/ # Seed management
│       └── types/          # Type definitions
├── tests/                   # Test suite
│   ├── test_controllers/    # Controller tests
│   ├── test_plant/         # Plant model tests
│   ├── test_simulation/    # Simulation tests
│   └── test_integration/   # End-to-end tests
├── docs/                    # Documentation
│   ├── reference/          # API documentation
│   ├── guides/             # User guides
│   └── theory/            # Mathematical background
├── notebooks/               # Jupyter analysis notebooks
├── benchmarks/              # Performance benchmarks
├── config/                  # Configuration schemas
└── .dev_tools/              # Development utilities
```

## Testing

### Coverage Requirements

**MANDATORY TESTING POLICY**: All new code MUST include comprehensive testing:

#### Coverage Targets
- **Overall Project**: Minimum 85% test coverage
- **Critical Components**: Minimum 95% test coverage
  - Controllers (base classes, SMC algorithms, MPC)
  - Plant models (full, simplified, low-rank)
  - Simulation engines (integrators, orchestrators, safety)
- **Safety-Critical**: 100% test coverage REQUIRED
  - Control system safety mechanisms
  - Simulation numerical stability
  - Plant physical constraint validation

#### Test Development Workflow
1. **BEFORE coding**: Write test specifications
2. **DURING coding**: Implement tests alongside code
3. **AFTER coding**: Validate 100% of new functionality is tested
4. **CONTINUOUS**: Maintain and update tests for changes

### Running Tests

```bash
# Full test suite
python -m pytest

# Specific test categories
pytest tests/test_controllers/     # Controller tests
pytest tests/test_integration/     # Integration tests
pytest --benchmark-only            # Performance benchmarks

# Coverage analysis
pytest --cov=src --cov-report=html
```

### Test Structure

```
tests/
├── test_controllers/
│   ├── base/                    # Controller interface tests
│   └── smc/
│       ├── core/               # SMC mathematical components
│       └── classical/          # Classical SMC implementation
├── test_plant/
│   └── models/                 # Plant dynamics testing
├── test_simulation/
│   └── engines/                # Simulation execution testing
└── test_*.py                   # Component-specific test suites
```

## Performance Benchmarks

This project includes automated performance tests powered by **pytest-benchmark**.

### Running Benchmarks
```bash
# Run only benchmarks
pytest --benchmark-only --benchmark-autosave

# Compare against baseline and fail on regressions
pytest --benchmark-only --benchmark-compare --benchmark-compare-fail=mean:5%
```

### What Gets Measured
- **Controller microbenchmarks**: `compute_control` for each controller type
- **End-to-end throughput**: Batch simulation for 50 particles over 1.0s
- **Memory usage**: Peak memory consumption during simulations
- **Integration accuracy**: Numerical error accumulation

## Development & Contributing

### Code Quality

```bash
# Type checking
mypy src/

# Code formatting
black src/ tests/

# Linting
ruff src/ tests/

# Pre-commit hooks
pre-commit install
pre-commit run --all-files
```

### Documentation

```bash
# Build documentation
sphinx-build -b html docs docs/_build/html

# Serve locally
python -m http.server -d docs/_build/html
```

### Performance Profiling

```bash
# Benchmark specific components
pytest tests/test_benchmarks/ --benchmark-only

# Profile memory usage
python -m memory_profiler simulate.py --ctrl classical_smc

# Generate performance report
python .dev_tools/performance_audit.py
```

## Configuration Reference

The system uses YAML configuration with comprehensive validation:

```yaml
# config.yaml
physics:
  cart_mass: 1.0        # Cart mass (kg)
  pole1_mass: 0.1       # First pole mass (kg)
  pole2_mass: 0.1       # Second pole mass (kg)
  pole1_length: 0.5     # First pole length (m)
  pole2_length: 0.5     # Second pole length (m)

controllers:
  classical_smc:
    k1: 50.0            # Sliding surface gain 1
    k2: 25.0            # Sliding surface gain 2
    epsilon: 0.1        # Boundary layer width
    max_force: 10.0     # Maximum control force (N)

simulation:
  dt: 0.01              # Integration step (s)
  duration: 10.0        # Simulation time (s)
  initial_state: [0, 0, 0.1, 0, 0.1, 0]  # [x, ẋ, θ₁, θ̇₁, θ₂, θ̇₂]

optimization:
  pso:
    particles: 30       # Number of particles
    generations: 50     # Number of generations
    w: 0.729           # Inertia weight
    c1: 1.494          # Cognitive coefficient
    c2: 1.494          # Social coefficient
```

## Research Applications

### Control Theory Research
- **Lyapunov Stability Analysis**: Automated stability verification
- **Chattering Reduction**: Boundary layer and higher-order SMC
- **Robustness Testing**: Monte Carlo uncertainty analysis
- **Adaptive Control**: Online parameter estimation

### Educational Use
- **Interactive Simulations**: Real-time parameter exploration
- **Visualization Tools**: Phase portraits, control effort plots
- **Comparative Studies**: Multiple controller performance
- **Mathematical Validation**: Theoretical property verification

### Industrial Applications
- **Hardware-in-the-Loop**: Real-time system integration
- **Fault Detection**: Automated anomaly detection
- **Parameter Optimization**: Automated gain tuning
- **Performance Monitoring**: Continuous system health assessment

## Performance Features

- **Numba Acceleration**: JIT compilation for critical loops
- **Vectorized Operations**: Parallel batch simulations
- **Memory Efficiency**: Optimized data structures
- **Benchmark Suite**: Automated performance regression detection

## Safety & Reliability

- **Numerical Stability**: Robust handling of ill-conditioned dynamics
- **Constraint Monitoring**: Real-time safety boundary enforcement
- **Error Recovery**: Graceful degradation mechanisms
- **Input Validation**: Comprehensive parameter checking

## Production Readiness

**Current Status: 6.1/10** (Single-threaded operation recommended)

### Verified Components
- **Dependency Safety**: numpy 2.0 compatibility verified
- **Memory Safety**: Bounded collections with cleanup mechanisms
- **Single Point of Failure**: DI/factory registry with resilient config
- **Configuration Validation**: Strict YAML schema validation

### Known Limitations
- **Thread Safety**: Multi-threaded operation not recommended
- **Production Deployment**: Requires single-threaded configuration

### Validation Commands
```bash
python scripts/verify_dependencies.py
python scripts/test_memory_leak_fixes.py
python scripts/test_spof_fixes.py
```

## License & Citation

```
MIT License - see LICENSE file for details
```

**Citation:**
```bibtex
@software{dip_smc_pso,
  title={Double-Inverted Pendulum Sliding Mode Control with PSO Optimization},
  author={Your Name},
  url={https://github.com/theSadeQ/dip-smc-pso},
  year={2024}
}
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## Support

- **Documentation**: [Read the Docs](https://dip-smc-pso.readthedocs.io/)
- **Issues**: [GitHub Issues](https://github.com/theSadeQ/dip-smc-pso/issues)
- **Discussions**: [GitHub Discussions](https://github.com/theSadeQ/dip-smc-pso/discussions)

---

**Built for the control systems community**