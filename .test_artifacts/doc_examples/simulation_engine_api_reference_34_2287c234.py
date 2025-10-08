# Example from: docs\api\simulation_engine_api_reference.md
# Index: 34
# Runnable: True
# Hash: 2287c234

def get_state_dimension(self) -> int:
    """Get state vector dimension (default: 6 for DIP)."""
    return 6

def get_control_dimension(self) -> int:
    """Get control input dimension (default: 1 for DIP)."""
    return 1