# Example from: docs\mathematical_foundations\advanced_algorithms_guide.md
# Index: 5
# Runnable: True
# Hash: 4d11959d

from src.controllers.smc.algorithms.super_twisting.twisting_algorithm import SuperTwistingAlgorithm

# Initialize STA
sta = SuperTwistingAlgorithm(
    K1=5.0,                    # First twisting gain
    K2=4.0,                    # Second twisting gain (K1 > K2)
    alpha=0.5,                 # Standard power exponent
    anti_windup_limit=10.0,    # Bound integral state
    regularization=1e-10       # Numerical safety
)

# Compute control at each timestep
dt = 0.01  # 10 ms timestep

for t in time_array:
    # Compute sliding surface (from SMC controller)
    s = sliding_surface(state)

    # Super-twisting control law
    control_dict = sta.compute_control(
        surface_value=s,
        dt=dt,
        switching_function='tanh',
        boundary_layer=0.01
    )

    # Extract components
    u_total = control_dict['u_total']
    u1 = control_dict['u1_continuous']
    u2 = control_dict['u2_integral']

    # Apply control
    state = plant.step(u_total, dt)