# Example from: docs\controllers\mpc_technical_guide.md
# Index: 10
# Runnable: False
# Hash: 238920a5

@dataclass
class MPCWeights:
    """Cost function weights for MPC optimization."""
    q_x: float = 1.0          # Cart position
    q_theta: float = 10.0     # Pendulum angles
    q_xdot: float = 0.1       # Cart velocity
    q_thetadot: float = 0.5   # Angular velocities
    r_u: float = 1e-2         # Input effort

class MPCController:
    """Linear MPC for double-inverted pendulum."""

    def __init__(
        self,
        dynamics_model: DoubleInvertedPendulum,
        horizon: int = 20,
        dt: float = 0.02,
        weights: Optional[MPCWeights] = None,
        max_force: float = 20.0,
        max_cart_pos: float = 2.4,
        max_theta_dev: float = 0.5,
        use_exact_discretization: bool = True,
        fallback_smc_gains: Optional[List[float]] = None,
        fallback_pd_gains: Optional[Tuple[float, float]] = None,
        max_du: Optional[float] = None
    ):
        """Initialize MPC controller with configuration."""
        ...

    def compute_control(self, t: float, x₀: np.ndarray) -> float:
        """Solve MPC QP and return optimal control."""
        ...

    def _safe_fallback(self, x₀: np.ndarray) -> float:
        """Fallback controller when QP fails."""
        ...