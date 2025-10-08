# Example from: docs\analysis\CONTROLLER_FACTORY_ANALYSIS.md
# Index: 2
# Runnable: True
# Hash: 0622d928

def compute_control(self, state: np.ndarray, last_control: float, history: Dict) -> Union[Dict, float]:
    """Universal controller interface for all SMC variants"""

@property
def gains(self) -> List[float]:
    """Required PSO interface - return controller gains"""

def reset(self) -> None:
    """Reset controller to initial state"""