#======================================================================================
#=========== src/controllers/smc/algorithms/regional_hybrid/controller.py ============
#======================================================================================

"""
Regional Hybrid SMC Controller - Main Implementation.

Combines Adaptive SMC baseline with regional super-twisting enhancement.
Avoids B_eq singularities through safe region checking.

Architecture:
    - Base: Adaptive SMC (0.036 chattering - proven)
    - Enhancement: Super-twisting applied ONLY in safe regions
    - Safety: Three conditions must ALL be met to enable STA
"""

from typing import Dict, List, Optional, Any
import numpy as np
import logging

from .config import RegionalHybridConfig
from .safety_checker import (
    is_safe_for_supertwisting,
    compute_blend_weight,
)

logger = logging.getLogger(__name__)


class RegionalHybridController:
    """
    Regional Hybrid SMC Controller.

    Uses Adaptive SMC as baseline, adds super-twisting only in safe regions
    where B_eq singularities cannot occur.

    State Format: [x, θ₁, θ₂, ẋ, θ̇₁, θ̇₂]
    """

    # Required for PSO optimization integration
    n_gains = 4  # [k1, k2, lambda1, lambda2] for baseline surface

    def __init__(self, config: RegionalHybridConfig, dynamics=None, **kwargs):
        """
        Initialize Regional Hybrid SMC controller.

        Args:
            config: Type-safe configuration object
            dynamics: Optional dynamics model (for compatibility)
            **kwargs: Additional parameters for compatibility
        """
        self.config = config
        self.dynamics = dynamics

        # Extract gains from kwargs if provided (PSO compatibility)
        gains = kwargs.get("gains", None)
        if gains is not None and len(gains) >= 4:
            self.gains = np.array(gains[:4])
        else:
            # Default gains (will be optimized by PSO)
            self.gains = np.array([20.0, 15.0, 9.0, 4.0])

        logger.info(
            f"Initialized Regional Hybrid Controller with gains: {self.gains}"
        )

        # TODO Phase 2: Initialize sub-controllers
        # self.adaptive_smc = ModularAdaptiveSMC(...)
        # self.super_twisting = SuperTwistingAlgorithm(...)

        # Statistics tracking
        self.stats = {
            "total_steps": 0,
            "sta_active_steps": 0,
            "unsafe_conditions": 0,
        }

    def compute_control(
        self,
        state: np.ndarray,
        t: float,
        last_control: Optional[float] = None,
        **kwargs
    ) -> float:
        """
        Compute control output with regional super-twisting.

        Args:
            state: State vector [x, θ₁, θ₂, ẋ, θ̇₁, θ̇₂]
            t: Current time (s)
            last_control: Previous control value (for STA integral)
            **kwargs: Additional parameters

        Returns:
            u: Control force (N)
        """
        self.stats["total_steps"] += 1

        # TODO Phase 2: Implement full control law
        # Step 1: Compute base Adaptive SMC control
        # u_adaptive = self.adaptive_smc.compute_control(state, t, last_control)

        # Step 2: Check if super-twisting is SAFE to apply
        # is_safe, diagnostics = is_safe_for_supertwisting(
        #     state, self.gains,
        #     self.config.angle_threshold,
        #     self.config.surface_threshold,
        #     self.config.B_eq_threshold
        # )

        # Step 3: If safe, blend with super-twisting
        # if is_safe:
        #     self.stats["sta_active_steps"] += 1
        #     u_sta = self.super_twisting.compute_control(state, t, last_control)
        #     blend_weight = compute_blend_weight(...)
        #     u_final = (1 - blend_weight) * u_adaptive + blend_weight * u_sta
        # else:
        #     self.stats["unsafe_conditions"] += 1
        #     u_final = u_adaptive  # Safe fallback

        # Placeholder for Phase 1 (return zero control)
        u_final = 0.0

        # Saturate control
        u_saturated = np.clip(u_final, -self.config.max_force, self.config.max_force)

        return u_saturated

    def reset(self):
        """Reset controller state."""
        # TODO Phase 2: Reset sub-controllers
        # self.adaptive_smc.reset()
        # self.super_twisting.reset()

        # Reset statistics
        self.stats = {
            "total_steps": 0,
            "sta_active_steps": 0,
            "unsafe_conditions": 0,
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get controller statistics."""
        if self.stats["total_steps"] > 0:
            sta_usage_percent = (
                100.0 * self.stats["sta_active_steps"] / self.stats["total_steps"]
            )
        else:
            sta_usage_percent = 0.0

        return {
            **self.stats,
            "sta_usage_percent": sta_usage_percent,
        }
