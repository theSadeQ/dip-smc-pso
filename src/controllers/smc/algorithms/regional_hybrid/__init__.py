#======================================================================================
#============ src/controllers/smc/algorithms/regional_hybrid/__init__.py =============
#======================================================================================

"""
Regional Hybrid SMC Controller Module.

Implements the Regional Hybrid Architecture that combines:
- Adaptive SMC baseline (proven 0.036 chattering performance)
- Super-twisting enhancement applied ONLY in safe regions
- Avoids B_eq singularities through regional activation

This architecture addresses the fundamental incompatibility discovered in
the full-state Hybrid Adaptive STA-SMC (Gemini's theoretical proof).
"""

from .config import RegionalHybridConfig
from .controller import RegionalHybridController

__all__ = [
    "RegionalHybridConfig",
    "RegionalHybridController",
]
