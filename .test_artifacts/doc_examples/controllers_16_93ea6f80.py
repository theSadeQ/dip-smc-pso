# Example from: docs\guides\api\controllers.md
# Index: 16
# Runnable: True
# Hash: 93ea6f80

# In src/controllers/factory/__init__.py
from .my_custom_controller import TerminalSMC

_CONTROLLER_REGISTRY = {
    'classical_smc': ClassicalSMC,
    'sta_smc': SuperTwistingSMC,
    'adaptive_smc': AdaptiveSMC,
    'hybrid_adaptive_sta_smc': HybridAdaptiveSTASMC,
    'terminal_smc': TerminalSMC,  # Add custom controller
}