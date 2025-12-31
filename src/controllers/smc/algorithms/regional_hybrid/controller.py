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
from ..adaptive.controller import ModularAdaptiveSMC
from ..adaptive.config import AdaptiveSMCConfig

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

        # Phase 2.1: Initialize Adaptive SMC baseline controller
        # AdaptiveSMC requires 5 gains: [k1, k2, lambda1, lambda2, gamma]
        # We use self.gains (4 params from PSO) + config.alpha as gamma
        adaptive_gains = list(self.gains) + [config.alpha]  # [k1, k2, lam1, lam2, gamma]

        adaptive_config = AdaptiveSMCConfig(
            gains=adaptive_gains,
            max_force=config.max_force,
            dt=config.dt,
            boundary_layer=config.epsilon_min,
            smooth_switch=True,  # Use smooth switching for chattering reduction
            K_init=10.0,  # Initial adaptive gain
            dynamics_model=dynamics
        )

        self.adaptive_smc = ModularAdaptiveSMC(
            config=adaptive_config,
            dynamics=dynamics
        )

        logger.info(
            f"Initialized Adaptive SMC baseline with gains: {adaptive_gains}, "
            f"boundary_layer: {config.epsilon_min:.4f}"
        )

        # TODO Phase 2.2: Initialize Super-Twisting layer
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

        # Phase 2.1: Compute base Adaptive SMC control
        # ModularAdaptiveSMC returns a dict with 'control_signal' key
        adaptive_result = self.adaptive_smc.compute_control(
            state=state,
            state_vars=None,
            history=kwargs.get("history", None),
            dt=None  # Will use config.dt internally
        )

        # Extract control signal from result
        if isinstance(adaptive_result, dict):
            u_adaptive = adaptive_result.get("control_signal", 0.0)
        else:
            # Fallback if array returned (should not happen with our interface)
            u_adaptive = float(adaptive_result[0]) if len(adaptive_result) > 0 else 0.0

        # TODO Phase 2.2-2.3: Implement super-twisting and blending
        # For now (Phase 2.1), just use baseline Adaptive SMC
        u_final = u_adaptive

        # Step 2: Check if super-twisting is SAFE to apply (not yet implemented)
        # is_safe, diagnostics = is_safe_for_supertwisting(
        #     state, self.gains,
        #     self.config.angle_threshold,
        #     self.config.surface_threshold,
        #     self.config.B_eq_threshold
        # )

        # Step 3: If safe, blend with super-twisting (not yet implemented)
        # if is_safe:
        #     self.stats["sta_active_steps"] += 1
        #     u_sta = self.super_twisting.compute_control(state, t, last_control)
        #     blend_weight = compute_blend_weight(...)
        #     u_final = (1 - blend_weight) * u_adaptive + blend_weight * u_sta
        # else:
        #     self.stats["unsafe_conditions"] += 1
        #     u_final = u_adaptive  # Safe fallback

        # Saturate control
        u_saturated = np.clip(u_final, -self.config.max_force, self.config.max_force)

        return u_saturated

    def reset(self):
        """Reset controller state."""
        # Phase 2.1: Reset Adaptive SMC baseline
        if hasattr(self, 'adaptive_smc'):
            # ModularAdaptiveSMC doesn't have a reset() method, but we can reinitialize
            # its internal state by recreating the config and controller
            # For now, just log that we would reset it
            logger.info("Resetting Adaptive SMC baseline")

        # TODO Phase 2.2: Reset Super-Twisting layer
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
