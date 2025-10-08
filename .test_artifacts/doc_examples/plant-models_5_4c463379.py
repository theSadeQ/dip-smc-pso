# Example from: docs\guides\api\plant-models.md
# Index: 5
# Runnable: True
# Hash: 4c463379

from src.config.schemas import DIPParams

# Define custom parameters
custom_params = DIPParams(
    m0=2.0,      # Heavier cart
    m1=0.3,      # Lighter first pendulum
    m2=0.5,      # Lighter second pendulum
    l1=0.4,      # Shorter first link
    l2=0.6,      # Shorter second link
    b0=0.2,      # Higher cart friction
    b1=0.02,     # Higher joint friction
    b2=0.02,
    g=9.81
)

# Inertias auto-calculated: I = (1/3) * m * l²
print(f"I1 (auto): {custom_params.I1:.4f} kg⋅m²")
print(f"I2 (auto): {custom_params.I2:.4f} kg⋅m²")