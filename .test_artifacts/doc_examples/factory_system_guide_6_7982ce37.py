# Example from: docs\controllers\factory_system_guide.md
# Index: 6
# Runnable: False
# Hash: 7982ce37

# example-metadata:
# runnable: false

CONTROLLER_ALIASES = {
    'classic_smc': 'classical_smc',
    'smc_classical': 'classical_smc',
    'smc_v1': 'classical_smc',
    'super_twisting': 'sta_smc',
    'sta': 'sta_smc',
    'adaptive': 'adaptive_smc',
    'hybrid': 'hybrid_adaptive_sta_smc',
}

# All these create the same controller:
create_controller('classical_smc', ...)
create_controller('classic_smc', ...)
create_controller('smc_classical', ...)