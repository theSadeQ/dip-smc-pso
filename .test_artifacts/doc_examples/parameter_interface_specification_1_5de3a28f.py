# Example from: docs\factory\parameter_interface_specification.md
# Index: 1
# Runnable: False
# Hash: 5de3a28f

def _resolve_controller_gains(
    gains: Optional[Union[List[float], np.ndarray]],
    config: Optional[Any],
    controller_type: str,
    controller_info: Dict[str, Any]
) -> List[float]:
    """
    Resolve controller gains from multiple sources with intelligent fallback.

    Resolution Order:
    1. Explicit gains parameter (if provided)
    2. Configuration object gains extraction
    3. Registry default gains
    """

    # Priority 1: Explicit gains
    if gains is not None:
        if isinstance(gains, np.ndarray):
            gains = gains.tolist()
        return gains

    # Priority 2: Configuration extraction
    if config is not None:
        try:
            # Pattern A: config.controller_defaults structure
            if hasattr(config, 'controller_defaults'):
                defaults = config.controller_defaults
                if isinstance(defaults, dict) and controller_type in defaults:
                    config_gains = defaults[controller_type].get('gains')
                    if config_gains is not None:
                        return config_gains

            # Pattern B: config.controllers structure
            elif hasattr(config, 'controllers'):
                controllers = config.controllers
                if isinstance(controllers, dict) and controller_type in controllers:
                    config_gains = controllers[controller_type].get('gains')
                    if config_gains is not None:
                        return config_gains

        except Exception:
            pass  # Fall through to default gains

    # Priority 3: Registry defaults
    return controller_info['default_gains']