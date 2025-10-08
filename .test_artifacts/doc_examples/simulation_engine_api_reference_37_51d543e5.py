# Example from: docs\api\simulation_engine_api_reference.md
# Index: 37
# Runnable: True
# Hash: 51d543e5

from src.plant.models.lowrank import LowRankDIPConfig, LowRankDIPDynamics

# Create default configuration
config = LowRankDIPConfig.create_default()

# Or load from dictionary
config = LowRankDIPConfig.from_dict({
    'cart_mass': 1.0,
    'pole1_mass': 0.1,
    'pole2_mass': 0.1,
    'pole1_length': 0.5,
    'pole2_length': 0.5,
    'gravity': 9.81,
    'damping_cart': 0.01,
    'damping_pole1': 0.001,
    'damping_pole2': 0.001
})

# Initialize dynamics
dynamics = LowRankDIPDynamics(
    config=config,
    enable_monitoring=True,   # Track performance statistics
    enable_validation=True    # Enable state validation
)