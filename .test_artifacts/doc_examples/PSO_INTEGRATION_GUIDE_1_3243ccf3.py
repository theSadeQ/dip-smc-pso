# Example from: docs\PSO_INTEGRATION_GUIDE.md
# Index: 1
# Runnable: True
# Hash: 3243ccf3

from src.controllers.factory import SMCType, create_smc_for_pso
from src.plant.configurations import ConfigurationFactory

# Create plant configuration
plant_config = ConfigurationFactory.create_default_config("simplified")

# Create controller with PSO-friendly interface
gains = [10.0, 5.0, 8.0, 3.0, 15.0, 2.0]  # 6 gains for Classical SMC
controller = create_smc_for_pso(SMCType.CLASSICAL, gains, plant_config)

# Use simplified control interface
state = np.array([0.1, 0.2, 0.3, 0.0, 0.0, 0.0])
control = controller.compute_control(state)  # Returns np.ndarray([control_value])