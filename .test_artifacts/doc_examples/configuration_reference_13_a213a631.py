# Example from: docs\factory\configuration_reference.md
# Index: 13
# Runnable: False
# Hash: a213a631

CONTROLLER_ALIASES = {
    'classic_smc': 'classical_smc',
    'smc_classical': 'classical_smc',
    'smc_v1': 'classical_smc',
    'super_twisting': 'sta_smc',
    'sta': 'sta_smc',
    'adaptive': 'adaptive_smc',
    'hybrid': 'hybrid_adaptive_sta_smc',
    'hybrid_sta': 'hybrid_adaptive_sta_smc',
}

def _canonicalize_controller_type(name: str) -> str:
    """Normalize controller type names for consistency."""
    if not isinstance(name, str):
        return name
    key = name.strip().lower().replace('-', '_').replace(' ', '_')
    return CONTROLLER_ALIASES.get(key, key)