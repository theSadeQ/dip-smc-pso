# Example from: docs\factory\factory_integration_user_guide.md
# Index: 17
# Runnable: True
# Hash: 66187ea5

# Good: Reuse controllers when possible
controller_cache = {}

def get_or_create_controller(controller_type, gains, config):
    cache_key = (controller_type, tuple(gains))

    if cache_key not in controller_cache:
        controller_cache[cache_key] = create_controller(
            controller_type, config=config, gains=gains
        )

    return controller_cache[cache_key]