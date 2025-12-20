"""
Utilities package for DIP-SMC-PSO project.

Reorganized structure (Week 2, December 2025):
- 14 subdirectories → 10 subdirectories
- Clearer domain organization
- Infrastructure, testing, control, monitoring domains

Modules:
    analysis: Statistical analysis and metrics
    control: Control engineering utilities (primitives, validation, types)
    infrastructure: Low-level system utilities (logging, memory, threading)
    monitoring: Runtime monitoring (realtime, metrics)
    numerical_stability: Safe numerical operations
    testing: Development and testing utilities (dev_tools, reproducibility, fault_injection)
    visualization: Plotting and animation utilities
"""

# Re-export main packages
from . import analysis
from . import control
from . import infrastructure
from . import monitoring
from . import numerical_stability
from . import testing
from . import visualization

__all__ = [
    'analysis',
    'control',
    'infrastructure',
    'monitoring',
    'numerical_stability',
    'testing',
    'visualization',
]

__version__ = '1.0.0'  # Post-reorganization
