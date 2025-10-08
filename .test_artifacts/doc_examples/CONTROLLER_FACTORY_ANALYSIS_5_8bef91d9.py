# Example from: docs\analysis\CONTROLLER_FACTORY_ANALYSIS.md
# Index: 5
# Runnable: True
# Hash: 8bef91d9

controller_factory = create_pso_controller_factory(SMCType.CLASSICAL, plant_config)
controller_factory.n_gains        # Required attribute
controller_factory.controller_type # Required attribute
controller_factory.max_force      # Required attribute