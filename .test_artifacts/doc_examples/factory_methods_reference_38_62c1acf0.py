# Example from: docs\api\factory_methods_reference.md
# Index: 38
# Runnable: True
# Hash: 62c1acf0

class SMCType(Enum):
    """SMC Controller types enumeration."""
    CLASSICAL = "classical_smc"
    ADAPTIVE = "adaptive_smc"
    SUPER_TWISTING = "sta_smc"
    HYBRID = "hybrid_adaptive_sta_smc"