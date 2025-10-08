# Example from: docs\api\factory_methods_reference.md
# Index: 29
# Runnable: True
# Hash: 4b463528

def _resolve_controller_gains(
    gains: Optional[Union[List[float], np.ndarray]],
    config: Optional[Any],
    controller_type: str,
    controller_info: Dict[str, Any]
) -> List[float]