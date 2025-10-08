# Example from: docs\reports\FACTORY_SYSTEM_ANALYSIS_REPORT.md
# Index: 2
# Runnable: True
# Hash: ca55cb02

# Factory creates PSO-compatible wrapper
pso_controller = create_smc_for_pso(SMCType.CLASSICAL, gains)
control_output = pso_controller.compute_control(state)  # Returns np.array