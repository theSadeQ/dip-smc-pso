# Example from: docs\api\factory_reference.md
# Index: 5
# Runnable: True
# Hash: 0ffe6197

from src.controllers.factory import SMCType

class SMCType(Enum):
    CLASSICAL = "classical_smc"
    ADAPTIVE = "adaptive_smc"
    SUPER_TWISTING = "sta_smc"
    HYBRID = "hybrid_adaptive_sta_smc"