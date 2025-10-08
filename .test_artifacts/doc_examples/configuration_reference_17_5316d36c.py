# Example from: docs\factory\configuration_reference.md
# Index: 17
# Runnable: True
# Hash: 5316d36c

# Backwards compatibility wrappers
def create_classical_smc_controller(config=None, gains=None) -> Any:
    return create_controller('classical_smc', config, gains)

def create_sta_smc_controller(config=None, gains=None) -> Any:
    return create_controller('sta_smc', config, gains)

def create_adaptive_smc_controller(config=None, gains=None) -> Any:
    return create_controller('adaptive_smc', config, gains)