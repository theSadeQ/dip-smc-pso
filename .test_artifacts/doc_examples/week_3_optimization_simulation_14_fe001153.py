# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 14
# Runnable: False
# Hash: fe001153

# 1. Define optimization problem
problem = OptimizationProblem(
    controller_type='classical_smc',
    bounds=[(0.1, 50)] * 6,
    objectives=['ise', 'chattering', 'effort'],
    weights=[0.5, 0.3, 0.2]
)

# 2. Create optimizer
optimizer = PSOCore(
    problem=problem,
    n_particles=30,
    max_iters=100
)

# 3. Run optimization
result = optimizer.optimize()

# 4. Validate with full dynamics
final_controller = create_controller(
    'classical_smc',
    gains=result.best_position,
    dynamics_model='full'
)

validation_result = simulate(final_controller, duration=10.0)

# 5. Save optimized gains
save_gains(result.best_position, 'optimized_classical_smc.json')