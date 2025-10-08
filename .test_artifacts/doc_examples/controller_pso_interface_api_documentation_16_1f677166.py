# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 16
# Runnable: False
# Hash: 1f677166

def robust_controller_factory(gains: np.ndarray,
                            controller_type: str,
                            fallback_gains: Optional[np.ndarray] = None) -> PSO_ControllerInterface:
    """Robust controller factory with error recovery.

    Parameters
    ----------
    gains : np.ndarray
        Primary gain vector
    controller_type : str
        Controller type
    fallback_gains : np.ndarray, optional
        Fallback gains for error recovery

    Returns
    -------
    PSO_ControllerInterface
        Controller instance (primary or fallback)

    Raises
    ------
    ControllerInstantiationError
        If both primary and fallback creation fail
    """
    try:
        # Validate gains first
        validation = ParameterValidator.validate_gain_vector(gains, controller_type)
        if not validation.is_valid:
            raise InvalidGainsError(gains, controller_type, '; '.join(validation.errors))

        # Create controller
        return ControllerFactory.create_controller(controller_type, gains)

    except Exception as e:
        if fallback_gains is not None:
            try:
                return ControllerFactory.create_controller(controller_type, fallback_gains)
            except Exception:
                pass

        raise ControllerInstantiationError(
            f"Failed to create {controller_type} controller: {str(e)}"
        ) from e