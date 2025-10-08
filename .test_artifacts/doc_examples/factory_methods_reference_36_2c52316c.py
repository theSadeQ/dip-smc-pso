# Example from: docs\api\factory_methods_reference.md
# Index: 36
# Runnable: True
# Hash: 2c52316c

# Type aliases for better type safety
StateVector = NDArray[np.float64]           # System state vector
ControlOutput = Union[float, NDArray[np.float64]]  # Control output
GainsArray = Union[List[float], NDArray[np.float64]]  # Gain values
ConfigDict = Dict[str, Any]                 # Configuration dictionary

# Generic type for controller instances
ControllerT = TypeVar('ControllerT')