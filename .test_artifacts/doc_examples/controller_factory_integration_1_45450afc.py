# Example from: docs\technical\controller_factory_integration.md
# Index: 1
# Runnable: True
# Hash: 45450afc

def create_controller(
    controller_type: str,
    config: Optional[Any] = None,
    gains: Optional[Union[list, np.ndarray]] = None
) -> Any