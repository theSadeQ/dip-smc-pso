# Example from: docs\pso_integration_technical_specification.md
# Index: 1
# Runnable: False
# Hash: a5271197

def controller_factory(gains: np.ndarray) -> Controller:
    """
    PSO-compatible controller factory interface.

    Mathematical Foundation:
    The factory must instantiate controllers with gain vector G ∈ ℝⁿ
    where n is controller-specific dimensionality:
    - Classical SMC: G ∈ ℝ⁶ (c₁, λ₁, c₂, λ₂, K, kd)
    - STA-SMC: G ∈ ℝ⁶ (K₁, K₂, k₁, k₂, λ₁, λ₂)
    - Adaptive SMC: G ∈ ℝ⁵ (c₁, λ₁, c₂, λ₂, γ)
    - Hybrid Adaptive STA-SMC: G ∈ ℝ⁴ (c₁, λ₁, c₂, λ₂)

    Parameters
    ----------
    gains : np.ndarray, shape (n,)
        Controller gain vector with validated bounds

    Returns
    -------
    Controller
        Configured SMC instance with required attributes:
        - max_force: float (actuator saturation limit)
        - validate_gains: Optional[Callable] (pre-filtering function)

    Interface Contracts
    ------------------
    1. Factory function MUST have attribute 'n_gains' specifying dimensionality
    2. Returned controller MUST implement control computation interface
    3. All gains MUST be positive and within specified bounds
    4. Controller MUST handle edge cases (singularities, saturation)
    """
    return create_controller(controller_type, config, gains=gains)

# Required factory attribute
controller_factory.n_gains = 6  # Controller-specific dimensionality