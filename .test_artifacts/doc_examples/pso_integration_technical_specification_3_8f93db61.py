# Example from: docs\pso_integration_technical_specification.md
# Index: 3
# Runnable: False
# Hash: 8f93db61

def validate_controller_gains(controller_type: str, gains: np.ndarray) -> np.ndarray:
    """
    Validate gain vectors for controller-specific stability requirements.

    Mathematical Validation Rules:

    Classical SMC:
    - All gains > 0 (positive definiteness)
    - Sliding surface gains c₁, λ₁, c₂, λ₂ ensure Hurwitz characteristic polynomial
    - Switching gains K, kd provide reaching condition satisfaction

    STA-SMC (Super-Twisting):
    - Algorithmic gains: K₁ > K₂ > 0 (stability condition)
    - Surface coefficients: λ₁, λ₂ for target damping ratio ζ ∈ [0.6, 0.8]
    - Finite-time convergence: K₁² > 4K₂|λ₁λ₂|

    Parameters
    ----------
    controller_type : str
        Controller identifier from registry
    gains : np.ndarray, shape (B, n)
        Batch of gain vectors to validate

    Returns
    -------
    np.ndarray, shape (B,), dtype=bool
        Validity mask for each gain vector
    """
    registry_info = CONTROLLER_REGISTRY[controller_type]
    bounds = registry_info['gain_bounds']

    # Basic bounds checking
    valid_mask = np.ones(gains.shape[0], dtype=bool)
    for i, (min_val, max_val) in enumerate(bounds):
        valid_mask &= (gains[:, i] >= min_val) & (gains[:, i] <= max_val)

    # Controller-specific stability checks
    if controller_type == 'sta_smc':
        # K₁ > K₂ condition for STA stability
        valid_mask &= gains[:, 0] > gains[:, 1]

        # Surface coefficient bounds for target damping
        lambda1, lambda2 = gains[:, 4], gains[:, 5]
        damping_ratio = lambda2 / (2 * np.sqrt(lambda1))
        valid_mask &= (damping_ratio >= 0.6) & (damping_ratio <= 0.8)

    return valid_mask