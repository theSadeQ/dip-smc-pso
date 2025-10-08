# Example from: docs\guides\api\controllers.md
# Index: 17
# Runnable: True
# Hash: 32220862

from my_custom_controller import TerminalSMC

# Direct instantiation
controller = TerminalSMC(
    gains=[10, 8, 15, 12, 50, 5, 7],
    max_force=100.0,
    alpha=0.5
)

# Or via factory (if registered)
from src.controllers import create_controller

controller = create_controller(
    'terminal_smc',
    config=terminal_smc_config
)