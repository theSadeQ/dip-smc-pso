# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 3
# Runnable: False
# Hash: ca28ded4

# These aliases are supported for backward compatibility
valid_names = {
    'classical_smc': ['classical_smc', 'classic_smc', 'smc_classical', 'smc_v1'],
    'sta_smc': ['sta_smc', 'super_twisting', 'sta'],
    'adaptive_smc': ['adaptive_smc', 'adaptive'],
    'hybrid_adaptive_sta_smc': ['hybrid_adaptive_sta_smc', 'hybrid', 'hybrid_sta']
}

# Use any valid name
controller = create_controller('classic_smc')      # ✅ Alias works
controller = create_controller('super_twisting')   # ✅ Alias works