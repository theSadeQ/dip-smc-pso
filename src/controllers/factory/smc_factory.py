#======================================================================================\\\
#======================= src/controllers/factory/smc_factory.py =======================\\\
#======================================================================================\\\

"""
Clean SMC Controller Factory - Focused on 4 Core SMC Controllers

Provides a unified, type-safe interface for creating SMC controllers optimized for:
- PSO parameter tuning
- Research consistency
- Performance benchmarking
- Clean separation of concerns

Design Principles:
- Single responsibility: Only SMC controllers
- Consistent interfaces: Unified parameter handling
- PSO-ready: Array-based parameter injection
- Type-safe: Explicit typing for all controllers
- Minimal: No unnecessary complexity
"""

# Standard library imports
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Protocol, Union, List, Optional, Type, Dict, Any, Tuple

# Third-party imports
import numpy as np

# Import the 4 core SMC controllers
try:
    from .smc.classic_smc import ClassicalSMC
    from .smc.adaptive_smc import AdaptiveSMC
    from .smc.sta_smc import SuperTwistingSMC
    from .smc.hybrid_adaptive_sta_smc import HybridAdaptiveSTASMC
except ImportError:
    # Fallback for different import contexts
    try:
        from src.controllers.smc.classic_smc import ClassicalSMC
        from src.controllers.smc.adaptive_smc import AdaptiveSMC
        from src.controllers.smc.sta_smc import SuperTwistingSMC
        from src.controllers.smc.hybrid_adaptive_sta_smc import HybridAdaptiveSTASMC
    except ImportError:
        # Final fallback - define dummy classes for demo
        class ClassicalSMC:
            def __init__(self, **kwargs: Any) -> None:
                self.gains = kwargs.get('gains', [])
        class AdaptiveSMC:
            def __init__(self, **kwargs: Any) -> None:
                self.gains = kwargs.get('gains', [])
        class SuperTwistingSMC:
            def __init__(self, **kwargs: Any) -> None:
                self.gains = kwargs.get('gains', [])
        class HybridAdaptiveSTASMC:
            def __init__(self, **kwargs: Any) -> None:
                self.gains = kwargs.get('gains', [])

# ============================================================================
# SMC CONTROLLER TYPES AND PROTOCOLS
# ============================================================================

class SMCType(Enum):
    """Enumeration of the 4 core SMC controller types."""
    CLASSICAL = "classical_smc"
    ADAPTIVE = "adaptive_smc"
    SUPER_TWISTING = "sta_smc"
    HYBRID = "hybrid_adaptive_sta_smc"

class SMCProtocol(Protocol):
    """Protocol defining the unified SMC controller interface."""

    def compute_control(self, state: np.ndarray, state_vars: Any, history: Dict[str, Any]) -> Any:
        """Compute control input for given state."""
        ...

    def initialize_state(self) -> Any:
        """Initialize controller internal state."""
        ...

    def initialize_history(self) -> Dict[str, Any]:
        """Initialize controller history tracking."""
        ...

    @property
    def gains(self) -> List[float]:
        """Return controller gains."""
        ...


class PSOControllerWrapper:
    """PSO-friendly wrapper that simplifies the control interface."""

    def __init__(self, controller: SMCProtocol):
        self.controller = controller
        self._history = {}     # Empty dict as default

        # Initialize appropriate state_vars based on controller type
        controller_name = type(controller).__name__
        if 'SuperTwisting' in controller_name or 'STA' in controller_name:
            # STA-SMC expects (z, sigma) tuple
            self._state_vars = (0.0, 0.0)  # Initial (z=0, sigma=0)
        elif 'Hybrid' in controller_name:
            # Hybrid controller expects (k1_prev, k2_prev, u_int_prev) tuple
            self._state_vars = (self.controller.k1_init, self.controller.k2_init, 0.0)
        else:
            # Classical and Adaptive SMC typically use empty tuple
            self._state_vars = ()

    def compute_control(self, state: np.ndarray, state_vars: Optional[Any] = None, history: Optional[Dict[str, Any]] = None) -> Union[np.ndarray, Any]:
        """
        Flexible compute_control interface supporting both patterns:
        1. compute_control(state) - PSO-friendly simplified interface
        2. compute_control(state, state_vars, history) - Full interface
        """
        # Use provided parameters or defaults
        final_state_vars = state_vars if state_vars is not None else self._state_vars
        final_history = history if history is not None else self._history

        result = self.controller.compute_control(state, final_state_vars, final_history)

        # For simplified interface (PSO usage), return numpy array
        if state_vars is None and history is None:
            # Extract control value from result - handle different output types
            if hasattr(result, 'u'):
                control_value = result.u
            elif hasattr(result, 'control'):
                control_value = result.control
            elif isinstance(result, dict) and 'u' in result:
                control_value = result['u']
            elif isinstance(result, dict) and 'control' in result:
                control_value = result['control']
            elif isinstance(result, tuple) and len(result) > 0:
                # Handle tuple returns (like early return from Hybrid controller)
                control_value = result[0]  # First element should be control value
            else:
                # Fallback: assume result is the control value
                control_value = result

            # Ensure numpy array output
            if isinstance(control_value, (int, float)):
                return np.array([control_value])
            elif isinstance(control_value, np.ndarray):
                return control_value.flatten()
            else:
                return np.array([float(control_value)])
        else:
            # For full interface, return original result
            return result

    @property
    def gains(self) -> List[float]:
        """Return controller gains."""
        return self.controller.gains

# ============================================================================
# CLEAN PARAMETER CONFIGURATION
# ============================================================================

@dataclass(frozen=True)
class SMCConfig:
    """Clean configuration for all SMC controllers."""

    # Core parameters (common to all SMCs)
    gains: List[float]
    max_force: float = 100.0
    dt: float = 0.01

    # Optional dynamics model
    dynamics_model: Optional[Any] = None

    # Controller-specific parameters (use defaults if not specified)
    boundary_layer: float = 0.01
    damping_gain: float = 0.0

    # Adaptive SMC specific
    leak_rate: float = 0.1
    adapt_rate_limit: float = 100.0
    K_min: float = 0.1
    K_max: float = 100.0
    K_init: float = 10.0
    dead_zone: float = 0.01
    smooth_switch: bool = True
    alpha: float = 0.5

    # Hybrid SMC specific
    k1_init: float = 5.0
    k2_init: float = 3.0
    gamma1: float = 0.5
    gamma2: float = 0.3

    def __post_init__(self) -> None:
        """Validate SMC configuration parameters."""
        if not self.gains or len(self.gains) == 0:
            raise ValueError("SMC gains cannot be empty")

        if self.max_force <= 0:
            raise ValueError("max_force must be positive")

        if self.dt <= 0:
            raise ValueError("dt must be positive")

        if self.boundary_layer <= 0:
            raise ValueError("boundary_layer must be positive")

        # Validate gain positivity (SMC stability requirement)
        if any(g <= 0 for g in self.gains[:4]):  # First 4 gains are typically surface gains
            raise ValueError("SMC surface gains must be positive for stability")

# ============================================================================
# GAIN SPECIFICATIONS FOR PSO
# ============================================================================

@dataclass(frozen=True)
class SMCGainSpec:
    """Specification of gain requirements for each SMC type."""
    controller_type: SMCType
    n_gains: int
    gain_names: List[str]
    description: str

    @property
    def gain_bounds(self) -> List[tuple[float, float]]:
        """Default gain bounds for PSO optimization."""
        if self.controller_type == SMCType.CLASSICAL:
            # [k1, k2, lam1, lam2, K, kd]
            return [(0.1, 50.0)] * 4 + [(1.0, 200.0)] + [(0.0, 50.0)]
        elif self.controller_type == SMCType.ADAPTIVE:
            # [k1, k2, lam1, lam2, gamma]
            return [(0.1, 50.0)] * 4 + [(0.01, 10.0)]
        elif self.controller_type == SMCType.SUPER_TWISTING:
            # [K1, K2, k1, k2, lam1, lam2]
            return [(1.0, 100.0)] * 2 + [(0.1, 50.0)] * 4
        elif self.controller_type == SMCType.HYBRID:
            # [c1, lambda1, c2, lambda2]
            return [(0.1, 50.0)] * 4
        else:
            raise ValueError(f"Unknown SMC type: {self.controller_type}")

# Pre-defined gain specifications
SMC_GAIN_SPECS: Dict[SMCType, SMCGainSpec] = {
    SMCType.CLASSICAL: SMCGainSpec(
        SMCType.CLASSICAL, 6,
        ["k1", "k2", "lam1", "lam2", "K", "kd"],
        "Classical SMC with switching and damping gains"
    ),
    SMCType.ADAPTIVE: SMCGainSpec(
        SMCType.ADAPTIVE, 5,
        ["k1", "k2", "lam1", "lam2", "gamma"],
        "Adaptive SMC with online gain adaptation"
    ),
    SMCType.SUPER_TWISTING: SMCGainSpec(
        SMCType.SUPER_TWISTING, 6,
        ["K1", "K2", "k1", "k2", "lam1", "lam2"],
        "Super-twisting algorithm with 2nd order sliding"
    ),
    SMCType.HYBRID: SMCGainSpec(
        SMCType.HYBRID, 4,
        ["c1", "lambda1", "c2", "lambda2"],
        "Hybrid adaptive super-twisting controller"
    )
}

# ============================================================================
# CLEAN SMC FACTORY
# ============================================================================

class SMCFactory:
    """
    Clean, focused factory for creating SMC controllers.

    Optimized for:
    - PSO parameter optimization
    - Research benchmarking
    - Type safety and consistency
    """

    @staticmethod
    def create_controller(
        smc_type: Union[SMCType, str],
        config: SMCConfig
    ) -> SMCProtocol:
        """
        Create an SMC controller with clean, validated configuration.

        Args:
            smc_type: Type of SMC controller to create
            config: Validated SMC configuration

        Returns:
            Initialized SMC controller

        Raises:
            ValueError: If controller type is invalid or configuration is invalid
        """
        # Normalize SMC type
        if isinstance(smc_type, str):
            try:
                smc_type = SMCType(smc_type.lower().replace("-", "_"))
            except ValueError:
                raise ValueError(f"Invalid SMC type: {smc_type}")

        # Validate gains for this controller type
        spec = SMC_GAIN_SPECS[smc_type]
        if len(config.gains) < spec.n_gains:
            raise ValueError(
                f"{smc_type.value} requires at least {spec.n_gains} gains, got {len(config.gains)}"
            )

        # Create controller based on type
        if smc_type == SMCType.CLASSICAL:
            return SMCFactory._create_classical_smc(config)
        elif smc_type == SMCType.ADAPTIVE:
            return SMCFactory._create_adaptive_smc(config)
        elif smc_type == SMCType.SUPER_TWISTING:
            return SMCFactory._create_super_twisting_smc(config)
        elif smc_type == SMCType.HYBRID:
            return SMCFactory._create_hybrid_smc(config)
        else:
            raise ValueError(f"Unsupported SMC type: {smc_type}")

    @staticmethod
    def create_from_gains(
        smc_type: Union[SMCType, str],
        gains: Union[List[float], np.ndarray],
        **kwargs: Any
    ) -> SMCProtocol:
        """
        PSO-friendly: Create controller directly from gains array.

        Args:
            smc_type: Type of SMC controller
            gains: Gain values as list or array
            **kwargs: Additional configuration parameters

        Returns:
            Initialized SMC controller
        """
        # Convert gains to list
        gains_list = list(np.asarray(gains).flatten())

        # Create configuration with gains and defaults
        config = SMCConfig(gains=gains_list, **kwargs)

        return SMCFactory.create_controller(smc_type, config)

    @staticmethod
    def get_gain_specification(smc_type: Union[SMCType, str]) -> SMCGainSpec:
        """Get gain specification for an SMC controller type."""
        if isinstance(smc_type, str):
            smc_type = SMCType(smc_type.lower().replace("-", "_"))
        return SMC_GAIN_SPECS[smc_type]

    @staticmethod
    def list_available_controllers() -> List[SMCType]:
        """List all available SMC controller types."""
        return list(SMCType)

    # ========================================================================
    # PRIVATE CONTROLLER CREATION METHODS
    # ========================================================================

    @staticmethod
    def _create_classical_smc(config: SMCConfig) -> ClassicalSMC:
        """Create Classical SMC with clean parameter mapping."""
        return ClassicalSMC(
            gains=config.gains,
            max_force=config.max_force,
            boundary_layer=config.boundary_layer,
            dynamics_model=config.dynamics_model
        )

    @staticmethod
    def _create_adaptive_smc(config: SMCConfig) -> AdaptiveSMC:
        """Create Adaptive SMC with clean parameter mapping."""
        return AdaptiveSMC(
            gains=config.gains,
            dt=config.dt,
            max_force=config.max_force,
            leak_rate=config.leak_rate,
            adapt_rate_limit=config.adapt_rate_limit,
            K_min=config.K_min,
            K_max=config.K_max,
            smooth_switch=config.smooth_switch,
            boundary_layer=config.boundary_layer,
            dead_zone=config.dead_zone,
            K_init=config.K_init,
            alpha=config.alpha
        )

    @staticmethod
    def _create_super_twisting_smc(config: SMCConfig) -> SuperTwistingSMC:
        """Create Super-Twisting SMC with clean parameter mapping."""
        return SuperTwistingSMC(
            gains=config.gains,
            dt=config.dt,
            max_force=config.max_force,
            damping_gain=config.damping_gain,
            boundary_layer=config.boundary_layer,
            dynamics_model=config.dynamics_model
        )

    @staticmethod
    def _create_hybrid_smc(config: SMCConfig) -> HybridAdaptiveSTASMC:
        """Create Hybrid Adaptive-STA SMC with clean parameter mapping."""
        return HybridAdaptiveSTASMC(
            gains=config.gains,
            dt=config.dt,
            max_force=config.max_force,
            k1_init=config.k1_init,
            k2_init=config.k2_init,
            gamma1=config.gamma1,
            gamma2=config.gamma2,
            dead_zone=config.dead_zone,
            dynamics_model=config.dynamics_model
        )

# ============================================================================
# CONVENIENCE FUNCTIONS FOR PSO INTEGRATION
# ============================================================================

def create_smc_for_pso(
    smc_type: Union[SMCType, str],
    gains: Union[List[float], np.ndarray],
    dynamics_model_or_max_force: Union[Any, float] = 100.0,
    dt: float = 0.01,
    dynamics_model: Optional[Any] = None
) -> PSOControllerWrapper:
    """
    Convenience function optimized for PSO parameter tuning.

    Supports both calling patterns:
    1. create_smc_for_pso(smc_type, gains, max_force, dt, dynamics_model)
    2. create_smc_for_pso(smc_type, gains, dynamics_model)

    Usage:
        # In PSO fitness function
        controller = create_smc_for_pso("classical_smc", pso_params)
        performance = evaluate_controller(controller, test_scenarios)
        return performance
    """
    # Handle different calling patterns
    if isinstance(dynamics_model_or_max_force, (int, float)):
        # Pattern 1: max_force provided as third argument
        max_force = float(dynamics_model_or_max_force)
        final_dynamics_model = dynamics_model
    else:
        # Pattern 2: dynamics_model provided as third argument
        max_force = 100.0  # Use default
        final_dynamics_model = dynamics_model_or_max_force

    controller = SMCFactory.create_from_gains(
        smc_type=smc_type,
        gains=gains,
        max_force=max_force,
        dt=dt,
        dynamics_model=final_dynamics_model
    )

    # Wrap controller for PSO-friendly interface
    wrapper = PSOControllerWrapper(controller)

    # Add PSO-required attributes to the wrapper
    spec = SMCFactory.get_gain_specification(smc_type)
    wrapper.n_gains = spec.n_gains
    wrapper.controller_type = smc_type.value if isinstance(smc_type, SMCType) else str(smc_type)

    return wrapper

def get_gain_bounds_for_pso(smc_type: Union[SMCType, str]) -> tuple[List[float], List[float]]:
    """Get PSO optimization bounds for SMC controller gains."""
    spec = SMCFactory.get_gain_specification(smc_type)
    bounds = spec.gain_bounds

    # Convert to PSO format: (lower_bounds, upper_bounds)
    lower_bounds = [bound[0] for bound in bounds]
    upper_bounds = [bound[1] for bound in bounds]

    return (lower_bounds, upper_bounds)

def validate_smc_gains(smc_type: Union[SMCType, str], gains: Union[List[float], np.ndarray]) -> bool:
    """Validate that gains are appropriate for the SMC controller type."""
    try:
        spec = SMCFactory.get_gain_specification(smc_type)
        gains_array = np.asarray(gains)

        # Check length
        if len(gains_array) < spec.n_gains:
            return False

        # Check positivity for surface gains (SMC stability requirement)
        if smc_type in [SMCType.CLASSICAL, SMCType.ADAPTIVE, SMCType.SUPER_TWISTING]:
            if any(g <= 0 for g in gains_array[:4]):  # First 4 are typically surface gains
                return False
        elif smc_type == SMCType.HYBRID:
            if any(g <= 0 for g in gains_array[:4]):  # All 4 gains must be positive
                return False

        return True
    except Exception:
        return False

# ============================================================================
# EXPORT CLEAN PUBLIC API
# ============================================================================

__all__ = [
    # Core types
    "SMCType",
    "SMCConfig",
    "SMCGainSpec",
    "SMCProtocol",

    # Factory
    "SMCFactory",

    # PSO wrapper
    "PSOControllerWrapper",

    # PSO convenience functions
    "create_smc_for_pso",
    "get_gain_bounds_for_pso",
    "validate_smc_gains",

    # Specifications
    "SMC_GAIN_SPECS"
]