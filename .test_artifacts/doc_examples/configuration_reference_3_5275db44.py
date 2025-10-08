# Example from: docs\factory\configuration_reference.md
# Index: 3
# Runnable: True
# Hash: 5275db44

def _resolve_controller_gains(
    gains: Optional[Union[List[float], np.ndarray]],
    config: Optional[Any],
    controller_type: str,
    controller_info: Dict[str, Any]
) -> List[float]:
    """Resolve controller gains from multiple sources with fallback."""