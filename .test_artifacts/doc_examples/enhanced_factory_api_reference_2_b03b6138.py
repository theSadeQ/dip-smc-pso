# Example from: docs\factory\enhanced_factory_api_reference.md
# Index: 2
# Runnable: True
# Hash: b03b6138

def create_controller(
    controller_type: str,
    config: Optional[Any] = None,
    gains: Optional[Union[List[float], np.ndarray]] = None
) -> Any