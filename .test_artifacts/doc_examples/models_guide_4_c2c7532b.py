# Example from: docs\plant\models_guide.md
# Index: 4
# Runnable: True
# Hash: c2c7532b

from src.plant.models.full import FullDIPDynamics, FullDIPConfig

# Create high-fidelity configuration
config = FullDIPConfig.create_default()

# Initialize with comprehensive monitoring
dynamics = FullDIPDynamics(
    config=config,
    enable_monitoring=True,
    enable_validation=True
)

# Compute dynamics with wind effects
wind_velocity = np.array([0.5, 0.0])  # 0.5 m/s horizontal wind
result = dynamics.compute_dynamics(
    state, control, time=1.5,
    wind_velocity=wind_velocity
)

# Access detailed diagnostics
if result.success:
    print(f"Total energy: {result.info['total_energy']:.4f} J")
    print(f"Cart kinetic: {result.info['kinetic_cart']:.4f} J")
    print(f"Friction forces: {result.info['friction_forces']}")
    print(f"Aerodynamic forces: {result.info['aerodynamic_forces']}")