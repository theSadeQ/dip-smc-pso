# Example from: docs\analysis\CONTROLLER_FACTORY_ANALYSIS.md
# Index: 6
# Runnable: True
# Hash: 46823409

controller = controller_factory(gains)
controller.validate_gains(particles)  # Batch gain validation
controller.compute_control(state)     # Control computation
controller.gains                      # Gain access for PSO