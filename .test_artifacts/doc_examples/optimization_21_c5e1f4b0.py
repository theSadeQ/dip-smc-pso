# Example from: docs\guides\api\optimization.md
# Index: 21
# Runnable: False
# Hash: c5e1f4b0

# example-metadata:
# runnable: false

# Coarse optimization with wide bounds
initial_bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
tuner_coarse = PSOTuner(SMCType.CLASSICAL, initial_bounds, n_particles=50, iters=50)
coarse_gains, _ = tuner_coarse.optimize()

# Fine optimization with narrow bounds around coarse solution
refined_bounds = [(g*0.8, g*1.2) for g in coarse_gains]
tuner_fine = PSOTuner(SMCType.CLASSICAL, refined_bounds, n_particles=30, iters=100)
fine_gains, fine_cost = tuner_fine.optimize()

print(f"Coarse gains: {coarse_gains}")
print(f"Fine gains: {fine_gains}")
print(f"Final cost: {fine_cost:.4f}")