# Example from: docs\technical\configuration_schema_reference.md
# Index: 12
# Runnable: True
# Hash: 907b5226

class HybridMode(Enum):
    """Hybrid controller operational modes."""
    CLASSICAL_ADAPTIVE = "classical_adaptive"   # Classical + Adaptive switching
    STA_ADAPTIVE = "sta_adaptive"              # STA + Adaptive switching
    FULL_HYBRID = "full_hybrid"                # All algorithms available