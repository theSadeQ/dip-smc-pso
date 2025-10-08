# Example from: docs\reports\factory_code_beautification_report.md
# Index: 8
# Runnable: False
# Hash: 8b9c489e

# example-metadata:
# runnable: false

# Backwards compatibility aliases
def create_classical_smc_controller(
    config: Optional[Any] = None,
    gains: Optional[Union[List[float], np.ndarray]] = None
) -> ControllerProtocol:
    """Create classical SMC controller (backwards compatibility)."""
    return create_controller('classical_smc', config, gains)

def create_controller_legacy(
    controller_type: str,
    config: Optional[Any] = None,
    gains: Optional[Union[List[float], np.ndarray]] = None
) -> ControllerProtocol:
    """Legacy factory function (backwards compatibility)."""
    return create_controller(controller_type, config, gains)