# Example from: docs\optimization_simulation\guide.md
# Index: 13
# Runnable: True
# Hash: 70d3bfa1

@model_validator(mode="after")
def _validate_com_within_length(self) -> "PhysicsConfig":
    if self.pendulum1_com >= self.pendulum1_length:
        raise ValueError(
            f"pendulum1_com must be < pendulum1_length (geometric requirement)"
        )
    return self