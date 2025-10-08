# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 17
# Runnable: False
# Hash: b9e55e5a

# example-metadata:
# runnable: false

# 1. Configure simulation
config = SimulationConfig(
    duration=5.0,
    dt=0.01,
    integrator='rk4',
    initial_state=np.array([0.1, 0.05, 0.0, 0.0, 0.0, 0.0])
)

# 2. Create components
dynamics = FullNonlinearDynamics(physics_params)
controller = create_controller('classical_smc', gains=[...])

# 3. Run simulation
runner = SimulationRunner(config)
result = runner.run(controller, dynamics)

# 4. Analyze results
print(f"ISE: {result.ise}")
print(f"Settling time: {result.settling_time}")