# Example from: docs\factory\deprecation_management.md
# Index: 1
# Runnable: True
# Hash: 752a46be

class DeprecationLevel(Enum):
    """Hierarchical deprecation severity levels."""
    INFO = "info"           # Informational - still fully supported
    WARNING = "warning"     # Will be removed in future versions
    ERROR = "error"         # Already removed, error fallback provided