# Example from: docs\guides\api\controllers.md
# Index: 2
# Runnable: True
# Hash: f90fc26a

from src.controllers import SMCType

# Available controller types
SMCType.CLASSICAL           # Classical sliding mode control
SMCType.SUPER_TWISTING      # Super-twisting algorithm (STA)
SMCType.ADAPTIVE            # Adaptive SMC with online gain tuning
SMCType.HYBRID              # Hybrid Adaptive STA-SMC