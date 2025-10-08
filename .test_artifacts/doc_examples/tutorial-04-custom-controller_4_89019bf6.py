# Example from: docs\guides\tutorials\tutorial-04-custom-controller.md
# Index: 4
# Runnable: False
# Hash: 89019bf6

from ..smc.terminal_smc import TerminalSMC  # Add import

class SMCType(str, Enum):
    CLASSICAL = "classical"
    ADAPTIVE = "adaptive"
    SUPER_TWISTING = "super_twisting"
    HYBRID = "hybrid"
    TERMINAL = "terminal"  # New controller type

# Update GAIN_SPECIFICATIONS
GAIN_SPECIFICATIONS = {
    # ... existing specs ...
    SMCType.TERMINAL: GainSpecification(
        controller_type=SMCType.TERMINAL,
        n_gains=7,
        gain_names=["k1", "k2", "lambda1", "lambda2", "K", "alpha", "beta"],
        bounds=[(0.1, 50.0), (0.1, 50.0), (0.1, 50.0), (0.1, 50.0),
                (1.0, 200.0), (0.1, 0.9), (0.1, 0.9)],
        description="Terminal SMC with nonlinear sliding surface"
    ),
}

# Update create_controller method
@staticmethod
def create_controller(
    controller_type: SMCType,
    config: SMCConfig,
    dynamics_model: Optional[Any] = None,
) -> Any:
    """Create SMC controller instance."""

    # ... existing code ...

    elif controller_type == SMCType.TERMINAL:
        from ..smc.terminal_smc import TerminalSMC
        return TerminalSMC(
            gains=config.gains,
            max_force=config.max_force,
            boundary_layer=config.boundary_layer,
            dynamics_model=dynamics_model,
            singularity_epsilon=getattr(config, 'singularity_epsilon', 1e-3),
            switch_method=getattr(config, 'switch_method', 'tanh'),
        )

    # ... rest of code ...