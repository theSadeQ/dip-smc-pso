# Example from: docs\reference\plant\core_state_validation.md
# Index: 3
# Runnable: True
# Hash: dac304c2

from src.plant.core.state_validation import ValidationConfig

# Custom validation constraints
validation_config = ValidationConfig(
    max_position=2.0,        # ±2m cart position
    max_angle=np.pi/2,       # ±90° joint angles
    max_velocity=5.0,        # 5 m/s cart velocity
    max_angular_velocity=10.0,  # 10 rad/s joint velocities
    energy_conservation_tol=0.05  # 5% energy drift tolerance
)

validator = StateValidator(validation_config)