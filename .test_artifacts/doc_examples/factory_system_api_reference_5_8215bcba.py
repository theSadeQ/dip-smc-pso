# Example from: docs\api\factory_system_api_reference.md
# Index: 5
# Runnable: False
# Hash: 8215bcba

# example-metadata:
# runnable: false

# Priority demonstration
config = load_config("config.yaml")  # config.controllers.classical_smc.gains = [5,5,5,0.5,0.5,0.5]

# Priority 1: Explicit gains override everything
controller = create_controller('classical_smc', config, gains=[10,10,10,1,1,1])
# Uses: [10,10,10,1,1,1]

# Priority 2: Config gains used when explicit gains not provided
controller = create_controller('classical_smc', config)
# Uses: [5,5,5,0.5,0.5,0.5] from config

# Priority 3: Registry defaults when config missing/invalid
controller = create_controller('classical_smc')
# Uses: [20.0, 15.0, 12.0, 8.0, 35.0, 5.0] from CONTROLLER_REGISTRY