# Example from: docs\factory_integration_documentation.md
# Index: 8
# Runnable: False
# Hash: 416e51eb

def _resolve_controller_gains(
    gains: Optional[Union[List[float], np.ndarray]],
    config: Optional[Any],
    controller_type: str,
    controller_info: Dict[str, Any]
) -> List[float]:
    """Resolve controller gains from multiple sources."""

    # Priority 1: Explicit gains
    if gains is not None:
        return gains.tolist() if isinstance(gains, np.ndarray) else gains

    # Priority 2: Configuration object
    if config is not None:
        extracted_gains = _extract_gains_from_config(config, controller_type)
        if extracted_gains is not None:
            return extracted_gains

    # Priority 3: Registry defaults
    return controller_info['default_gains']