# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 33
# Runnable: False
# Hash: 54850d16

# Ensure config.yaml has proper structure:
# controller_defaults:
#   classical_smc:
#     gains: [8.0, 6.0, 4.0, 3.0, 15.0, 2.0]
#
# controllers:
#   classical_smc:
#     max_force: 150.0
#     boundary_layer: 0.02

# Or provide gains explicitly:
controller = create_controller(
    controller_type='classical_smc',
    config=global_config,
    gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0]  # Override
)