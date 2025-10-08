# Example from: docs\factory\pso_factory_api_reference.md
# Index: 1
# Runnable: True
# Hash: 684ccc4f

# Core PSO-Factory integration
from controllers import (
    SMCType,                    # Controller type enumeration
    create_smc_for_pso,        # Primary PSO interface
    get_gain_bounds_for_pso,   # Mathematical bounds
    validate_smc_gains,        # Constraint validation
    PSOControllerWrapper       # PSO-optimized wrapper
)

# Advanced PSO workflows
from controllers.factory import (
    SMCFactory,                # Full factory interface
    SMCConfig,                 # Type-safe configuration
    SMCGainSpec               # Gain specifications
)

# Performance monitoring
from controllers.factory.monitoring import (
    PSOPerformanceMonitor,     # Real-time monitoring
    PSOBenchmarkSuite         # Comprehensive benchmarking
)