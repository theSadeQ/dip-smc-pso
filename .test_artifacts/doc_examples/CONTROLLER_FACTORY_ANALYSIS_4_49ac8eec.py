# Example from: docs\analysis\CONTROLLER_FACTORY_ANALYSIS.md
# Index: 4
# Runnable: True
# Hash: 49ac8eec

# In factory.py - _resolve_controller_gains function
if controller_type == 'hybrid_adaptive_sta_smc':
    # Extract surface gains from hybrid configuration
    if hasattr(config, 'gains'):
        return config.gains
    else:
        # Use default surface gains for hybrid controller
        return [18.0, 12.0, 10.0, 8.0]  # [c1, λ1, c2, λ2]