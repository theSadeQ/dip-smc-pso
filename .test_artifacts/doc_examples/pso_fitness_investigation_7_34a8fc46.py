# Example from: docs\testing\reports\2025-09-30\pso_fitness_investigation.md
# Index: 7
# Runnable: True
# Hash: 34a8fc46

# Diagnostic logging
if logger.isEnabledFor(logging.DEBUG):
    logger.debug(f"Cost components (normalized):")
    logger.debug(f"  ISE: {ise_n.mean():.6e}")
    logger.debug(f"  U²:  {u_n.mean():.6e}")
    logger.debug(f"  ΔU²: {du_n.mean():.6e}")
    logger.debug(f"  σ²:  {sigma_n.mean():.6e}")
    logger.debug(f"Total cost: {J.mean():.6e}")