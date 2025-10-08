# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 8
# Runnable: True
# Hash: 4985d41d

# Create controller with dynamic configuration override
controller = create_controller(
    controller_type='sta_smc',
    config=config,
    gains=[10.0, 5.0, 8.0, 6.0, 2.0, 1.5]  # Override config gains
)