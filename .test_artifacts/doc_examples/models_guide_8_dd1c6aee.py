# Example from: docs\plant\models_guide.md
# Index: 8
# Runnable: True
# Hash: dd1c6aee

# Total system mass
total_mass = config.get_total_mass()

# Characteristic length (max pendulum length)
L_char = config.get_characteristic_length()

# Characteristic time (natural period)
T_char = config.get_characteristic_time()  # sqrt(L/g)

# Natural frequency estimate
omega_n = config.estimate_natural_frequency()  # 1/T_char