# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 5
# Runnable: True
# Hash: 250abb84

# All these create the same classical SMC controller
controller1 = create_controller('classical_smc', gains)
controller2 = create_controller('classic_smc', gains)       # Alias
controller3 = create_controller('smc_classical', gains)     # Alias
controller4 = create_controller('smc_v1', gains)           # Alias

# STA-SMC aliases
controller5 = create_controller('sta_smc', gains)
controller6 = create_controller('super_twisting', gains)    # Alias
controller7 = create_controller('sta', gains)              # Alias