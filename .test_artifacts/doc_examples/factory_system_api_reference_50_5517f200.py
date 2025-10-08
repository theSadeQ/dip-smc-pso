# Example from: docs\api\factory_system_api_reference.md
# Index: 50
# Runnable: True
# Hash: 5517f200

def _canonicalize_controller_type(name: str) -> str:
    if not isinstance(name, str):
        raise ValueError(f"Controller type must be string, got {type(name)}")

    if not name.strip():
        raise ValueError("Controller type cannot be empty")

    key = name.strip().lower().replace('-', '_').replace(' ', '_')
    return CONTROLLER_ALIASES.get(key, key)