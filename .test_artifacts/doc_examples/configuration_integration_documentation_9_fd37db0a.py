# Example from: docs\configuration_integration_documentation.md
# Index: 9
# Runnable: False
# Hash: fd37db0a

# example-metadata:
# runnable: false

def _resolve_controller_gains(
    gains: Optional[Union[List[float], np.ndarray]],
    config: Optional[Any],
    controller_type: str,
    controller_info: Dict[str, Any]
) -> List[float]:
    """Resolve controller gains from multiple sources with priority."""

    # Priority 1: Explicit gains parameter
    if gains is not None:
        if isinstance(gains, np.ndarray):
            gains = gains.tolist()
        return gains

    # Priority 2: Configuration object extraction
    if config is not None:
        extracted_gains = _extract_gains_from_config(config, controller_type)
        if extracted_gains is not None:
            return extracted_gains

    # Priority 3: Registry defaults
    return controller_info['default_gains']

def _extract_gains_from_config(config: Any, controller_type: str) -> Optional[List[float]]:
    """Extract gains from configuration object using multiple patterns."""

    extraction_patterns = [
        # Pattern 1: config.controllers.controller_type.gains
        lambda: getattr(getattr(config.controllers, controller_type, None), 'gains', None),

        # Pattern 2: config.controllers[controller_type]['gains']
        lambda: config.controllers[controller_type]['gains'] if isinstance(config.controllers, dict) else None,

        # Pattern 3: config.controller_defaults.controller_type.gains
        lambda: getattr(getattr(config.controller_defaults, controller_type, None), 'gains', None),

        # Pattern 4: config.controller_defaults[controller_type]['gains']
        lambda: config.controller_defaults[controller_type]['gains'] if isinstance(config.controller_defaults, dict) else None,
    ]

    for pattern in extraction_patterns:
        try:
            gains = pattern()
            if gains is not None and isinstance(gains, (list, tuple)) and len(gains) > 0:
                return list(gains)
        except (AttributeError, KeyError, TypeError):
            continue

    return None