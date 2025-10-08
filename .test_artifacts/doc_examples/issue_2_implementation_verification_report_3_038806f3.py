# Example from: docs\reports\issue_2_implementation_verification_report.md
# Index: 3
# Runnable: False
# Hash: 038806f3

# All imports tested successfully:
from src.controllers.smc.sta_smc import SuperTwistingSMC          # ✅ Direct import
from src.controllers.sta_smc import SuperTwistingSMC             # ✅ Compatibility layer
from src.controllers import SuperTwistingSMC                     # ✅ Factory interface