# Example from: docs\mathematical_foundations\advanced_algorithms_guide.md
# Index: 6
# Runnable: False
# Hash: 1983c421

# Run simulation and collect surface history
surface_history = []

for t in time_array:
    s = sliding_surface(state)
    surface_history.append(s)

    control_dict = sta.compute_control(s, dt)
    state = plant.step(control_dict['u_total'], dt)

# Analyze STA performance
analysis = sta.analyze_performance(surface_history)

print("Stability Metrics:")
print(f"  Gains satisfy K1 > K2: {analysis['stability_metrics']['gains_satisfy_condition']}")
print(f"  Gain ratio K1/K2: {analysis['stability_metrics']['gain_ratio']:.2f}")

print("\nConvergence Metrics:")
print(f"  Convergence detected: {analysis['convergence_metrics']['convergence_detected']}")
print(f"  Convergence time steps: {analysis['convergence_metrics']['convergence_time_steps']}")
print(f"  Theoretical time: {analysis['convergence_metrics']['theoretical_convergence_time']:.3f} s")
print(f"  Final surface RMS: {analysis['convergence_metrics']['final_surface_rms']:.6f}")

print("\nControl Characteristics:")
print(f"  Integral state: {analysis['control_characteristics']['integral_state']:.3f}")
print(f"  Anti-windup active: {analysis['control_characteristics']['anti_windup_active']}")