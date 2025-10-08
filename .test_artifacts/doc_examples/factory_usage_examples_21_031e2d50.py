# Example from: docs\technical\factory_usage_examples.md
# Index: 21
# Runnable: True
# Hash: 031e2d50

"""Production-ready controller deployment workflow."""
from src.controllers.factory import create_controller, list_available_controllers
from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig
from src.config import load_config
import logging

# Step 1: Setup production logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Step 2: Load and validate configuration
config = load_config("config.yaml")

# Step 3: Create production controller with validated configuration
production_config = ClassicalSMCConfig(
    gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0],  # Validated stable gains
    max_force=150.0,                         # Hardware limit
    boundary_layer=0.02,                     # Tested boundary layer
    dt=0.001,                               # Control loop frequency
    switch_method="tanh",                    # Smooth switching
    regularization=1e-8                      # Numerical stability
)

# Step 4: Create controller with error handling
try:
    production_controller = create_controller(
        controller_type='classical_smc',
        config=production_config
    )

    logging.info("Production controller created successfully")

    # Step 5: Validate controller operation
    test_state = [0.0, 0.1, 0.05, 0.0, 0.0, 0.0]
    control_output = production_controller.compute_control(test_state, (), {})

    if hasattr(control_output, 'u'):
        control_value = control_output.u
    else:
        control_value = control_output

    logging.info(f"Controller validation successful: u = {control_value}")

except Exception as e:
    logging.error(f"Production controller creation failed: {e}")
    raise

print("Production deployment successful")