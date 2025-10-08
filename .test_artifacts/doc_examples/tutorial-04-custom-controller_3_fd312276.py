# Example from: docs\guides\tutorials\tutorial-04-custom-controller.md
# Index: 3
# Runnable: True
# Hash: fd312276

@dataclass(frozen=True)
class TerminalSMCOutput:
    """Output from Terminal SMC controller."""

    control: float
    sliding_surface: float
    switching_function: float
    terminal_term1: float  # sign(dθ₁)·|dθ₁|^α
    terminal_term2: float  # sign(dθ₂)·|dθ₂|^β