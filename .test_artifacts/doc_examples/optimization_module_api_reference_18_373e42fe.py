# Example from: docs\api\optimization_module_api_reference.md
# Index: 18
# Runnable: False
# Hash: 373e42fe

def validate_bounds(
    self,
    controller_type: str,
    lower_bounds: List[float],
    upper_bounds: List[float]
) -> BoundsValidationResult:
    """
    Validate PSO parameter bounds for specific controller type.

    Parameters
    ----------
    controller_type : str
        Controller type ('classical_smc', 'sta_smc', 'adaptive_smc', 'hybrid_adaptive_sta_smc')
    lower_bounds : List[float]
        Lower bounds for each parameter
    upper_bounds : List[float]
        Upper bounds for each parameter

    Returns
    -------
    BoundsValidationResult
        Validation result with warnings, recommendations, and adjusted bounds
    """