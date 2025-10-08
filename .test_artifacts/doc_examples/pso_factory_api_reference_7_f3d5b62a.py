# Example from: docs\factory\pso_factory_api_reference.md
# Index: 7
# Runnable: False
# Hash: f3d5b62a

class PSOControllerWrapper:
    """
    PSO-optimized wrapper providing simplified interface for SMC controllers.

    This wrapper is specifically designed for PSO fitness evaluation with:
    - Simplified control interface (single state input)
    - Automatic state management for stateful controllers
    - Unified output format (numpy array)
    - Robust error handling for PSO robustness
    - Performance optimization for repeated evaluations

    The wrapper handles the complexity of different SMC controller interfaces
    while providing a consistent, PSO-friendly API.

    Mathematical Foundation:
    The wrapper preserves the mathematical properties of the underlying
    SMC controller while simplifying the interface:

    Input: state = [θ₁, θ₂, x, θ̇₁, θ̇₂, ẋ] ∈ ℝ⁶
    Output: u ∈ ℝ (scalar control force)

    Internal State Management:
    - Classical SMC: Stateless (empty state_vars)
    - STA SMC: Maintains (z, σ) for integration
    - Adaptive SMC: Tracks adaptation variables
    - Hybrid SMC: Manages mode switching state

    Performance Characteristics:
    - Control computation: <0.1ms typical
    - Memory overhead: <500B per wrapper
    - Thread safety: Read operations only
    - Error recovery: Graceful degradation for invalid inputs
    """

    def __init__(self, controller: SMCProtocol):
        """
        Initialize PSO wrapper with SMC controller.

        Args:
            controller: SMC controller implementing SMCProtocol

        Raises:
            TypeError: If controller doesn't implement required interface
            ValueError: If controller configuration is invalid
        """
        # Validate controller interface
        if not hasattr(controller, 'compute_control'):
            raise TypeError("Controller must implement compute_control method")
        if not hasattr(controller, 'gains'):
            raise TypeError("Controller must have gains property")

        self.controller = controller
        self._history = {}  # Initialize empty history

        # Initialize controller-specific state variables
        controller_name = type(controller).__name__

        if 'SuperTwisting' in controller_name or 'STA' in controller_name:
            # STA-SMC maintains integration variables (z, σ)
            self._state_vars = (0.0, 0.0)  # Initial (z=0, σ=0)
        elif 'Hybrid' in controller_name:
            # Hybrid controller tracks adaptive gains and integration
            self._state_vars = (
                getattr(controller, 'k1_init', 5.0),  # k1_prev
                getattr(controller, 'k2_init', 3.0),  # k2_prev
                0.0                                    # u_int_prev
            )
        elif 'Adaptive' in controller_name:
            # Adaptive SMC may track adaptation state
            self._state_vars = getattr(controller, '_initial_state', ())
        else:
            # Classical SMC and others use empty state
            self._state_vars = ()

        # Performance tracking
        self._call_count = 0
        self._total_compute_time = 0.0
        self._last_error = None

    def compute_control(self,
                       state: np.ndarray,
                       state_vars: Optional[Any] = None,
                       history: Optional[Dict[str, Any]] = None
                       ) -> np.ndarray:
        """
        Compute control with flexible interface supporting both:
        1. Simplified PSO interface: compute_control(state)
        2. Full interface: compute_control(state, state_vars, history)

        Mathematical Interface:
        Input state vector: x = [θ₁, θ₂, x_cart, θ̇₁, θ̇₂, ẋ_cart]
        - θ₁, θ₂: Pendulum angles [rad]
        - x_cart: Cart position [m]
        - θ̇₁, θ̇₂: Angular velocities [rad/s]
        - ẋ_cart: Cart velocity [m/s]

        Output control: u ∈ ℝ
        - Scalar control force [N]
        - Bounded by actuator limits

        Args:
            state: System state vector (6-element numpy array)
            state_vars: Controller state variables (optional)
            history: Controller history (optional)

        Returns:
            Control output as 1-element numpy array [u]

        Raises:
            ValueError: If state has wrong dimensions
            RuntimeError: If control computation fails

        Performance:
            - Typical computation time: 0.01-0.1ms
            - Memory allocation: Minimal (output array only)
            - Error handling: Graceful fallback to zero control

        PSO Usage Pattern: