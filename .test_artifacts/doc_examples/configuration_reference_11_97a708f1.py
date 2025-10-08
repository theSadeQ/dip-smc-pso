# Example from: docs\factory\configuration_reference.md
# Index: 11
# Runnable: True
# Hash: 97a708f1

# Graceful handling of missing dependencies
try:
    from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig
    CONFIG_CLASSES_AVAILABLE = True
except ImportError:
    CONFIG_CLASSES_AVAILABLE = False
    # Use fallback minimal config classes
    from src.controllers.factory.fallback_configs import ClassicalSMCConfig