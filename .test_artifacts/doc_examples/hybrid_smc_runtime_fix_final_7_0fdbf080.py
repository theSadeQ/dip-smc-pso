# Example from: docs\troubleshooting\hybrid_smc_runtime_fix_final.md
# Index: 7
# Runnable: True
# Hash: 0fdbf080

# Runtime type checking
from typing import Union, TypeGuard

def is_valid_control_output(obj: Any) -> TypeGuard[HybridSTAOutput]:
    """Type guard for control output validation."""
    return (
        hasattr(obj, 'control') and
        hasattr(obj, 'state_vars') and
        hasattr(obj, 'history') and
        hasattr(obj, 'sliding_surface')
    )