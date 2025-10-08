# Example from: docs\troubleshooting\hybrid_smc_runtime_fix_final.md
# Index: 10
# Runnable: False
# Hash: dbdbb025

def compute_control(self, state: np.ndarray, ...) -> HybridSTAOutput:
    """Compute hybrid adaptive STA-SMC control action.

    Args:
        state: System state vector [θ₁, θ₂, x, θ̇₁, θ̇₂, ẋ]
        state_vars: Previous adaptive gains (k₁, k₂, u_int)
        history: Control history for logging

    Returns:
        HybridSTAOutput: Named tuple containing:
            - control: Control force [N]
            - state_vars: Updated adaptive gains
            - history: Updated control history
            - sliding_surface: Current sliding surface value

    Raises:
        ValueError: If state has invalid dimensions
        RuntimeError: If numerical instability detected

    Note:
        CRITICAL: This method MUST always return HybridSTAOutput.
        Never allow implicit None returns.
    """