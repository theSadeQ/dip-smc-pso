# Example from: docs\factory\parameter_interface_specification.md
# Index: 14
# Runnable: True
# Hash: 5baa100c

# Always validate before creation
   validate_smc_gains(controller_type, gains)

   # Use bounds checking
   bounds = get_gain_bounds_for_pso(controller_type)
   validate_parameter_ranges(gains, controller_type, bounds)

   # Test with small disturbances first
   test_controller_stability(controller, small_disturbance_state)