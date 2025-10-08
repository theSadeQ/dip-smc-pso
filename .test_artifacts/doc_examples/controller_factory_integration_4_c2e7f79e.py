# Example from: docs\technical\controller_factory_integration.md
# Index: 4
# Runnable: True
# Hash: c2e7f79e

def _canonicalize_controller_type(name: str) -> str:
    """Normalize and alias controller type names."""
    if not isinstance(name, str):
        return name
    key = name.strip().lower().replace('-', '_').replace(' ', '_')
    return ALIAS_MAP.get(key, key)