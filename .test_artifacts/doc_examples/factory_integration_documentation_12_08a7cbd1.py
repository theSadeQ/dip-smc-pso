# Example from: docs\factory_integration_documentation.md
# Index: 12
# Runnable: False
# Hash: 08a7cbd1

# Optional MPC controller import with graceful fallback
try:
    from src.controllers.mpc.controller import MPCController
    MPC_AVAILABLE = True
except ImportError:
    MPCController = None
    MPC_AVAILABLE = False
    logger.debug("MPC controller not available - optional dependency")

# Registry entry with availability check
if MPC_AVAILABLE:
    CONTROLLER_REGISTRY['mpc_controller'] = {
        'class': MPCController,
        'config_class': MPCConfig,
        # ... full configuration
    }
else:
    CONTROLLER_REGISTRY['mpc_controller'] = {
        'class': None,
        'config_class': UnavailableMPCConfig,
        'description': 'Model predictive controller (unavailable)',
        # ... placeholder configuration
    }