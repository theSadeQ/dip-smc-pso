# Example from: docs\factory\factory_api_reference.md
# Index: 8
# Runnable: True
# Hash: 628a0b58

StateVector = NDArray[np.float64]        # 6-element state vector [θ₁, θ₂, x, θ̇₁, θ̇₂, ẋ]
ControlOutput = Union[float, NDArray[np.float64]]  # Scalar or array control output
GainsArray = Union[List[float], NDArray[np.float64]]  # Controller gains
ConfigDict = Dict[str, Any]              # Configuration dictionary