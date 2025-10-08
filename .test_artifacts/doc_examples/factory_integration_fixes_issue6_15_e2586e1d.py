# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 15
# Runnable: True
# Hash: e2586e1d

class HybridMode(Enum):
    """Hybrid controller operational modes."""
    CLASSICAL_ADAPTIVE = "classical_adaptive"
    STA_ADAPTIVE = "sta_adaptive"
    FULL_HYBRID = "full_hybrid"