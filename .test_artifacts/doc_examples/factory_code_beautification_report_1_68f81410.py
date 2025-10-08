# Example from: docs\reports\factory_code_beautification_report.md
# Index: 1
# Runnable: True
# Hash: 68f81410

# Before: Weak typing
def create_controller(controller_type: str, config=None, gains=None):

# After: Strong typing with protocols
def create_controller(
    controller_type: str,
    config: Optional[Any] = None,
    gains: Optional[Union[List[float], np.ndarray]] = None
) -> ControllerProtocol: