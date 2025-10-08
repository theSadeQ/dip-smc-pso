# Example from: docs\reference\controllers\base_control_primitives.md
# Index: 1
# Runnable: True
# Hash: 5dcabf2f

from src.controllers.base.control_primitives import saturate

# Apply saturation to control signal
u_raw = 150.0  # Exceeds actuator limit
u_max = 100.0

u = saturate(u_raw, u_max)
print(f"Saturated control: {u:.1f} N")  # 100.0 N

# Vectorized saturation
u_raw_array = np.array([150.0, 50.0, -120.0, 30.0])
u_array = saturate(u_raw_array, u_max)
print(f"Saturated controls: {u_array}")  # [100, 50, -100, 30]