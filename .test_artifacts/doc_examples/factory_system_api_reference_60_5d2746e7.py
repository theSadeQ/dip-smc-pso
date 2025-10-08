# Example from: docs\api\factory_system_api_reference.md
# Index: 60
# Runnable: False
# Hash: 5d2746e7

# src/controllers/new_controller_config.py

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class NewControllerConfig:
    """Configuration for NewController."""

    gains: List[float]
    max_force: float
    dt: float
    # Additional parameters...

    def __post_init__(self):
        """Validate configuration."""
        if len(self.gains) != 4:  # Example: requires 4 gains
            raise ValueError("NewController requires 4 gains")
        if self.max_force <= 0:
            raise ValueError("max_force must be positive")
        if self.dt <= 0:
            raise ValueError("dt must be positive")