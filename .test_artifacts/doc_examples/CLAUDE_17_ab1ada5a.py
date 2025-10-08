# Example from: docs\CLAUDE.md
# Index: 17
# Runnable: True
# Hash: ab1ada5a

controller = ClassicalSMC(gains=[10,8,15,12,50,5], max_force=100, boundary_layer=0.01)
result = simulate(controller)
# Automatic cleanup