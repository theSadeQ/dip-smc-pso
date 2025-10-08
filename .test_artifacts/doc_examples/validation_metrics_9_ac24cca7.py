# Example from: docs\reference\analysis\validation_metrics.md
# Index: 9
# Runnable: False
# Hash: ac24cca7

# Track energy conservation (for unforced natural dynamics)
def compute_energy_drift(result, dynamics):
    """Measure energy drift as validation check."""
    energies = [dynamics.compute_total_energy(x) for x in result.states]
    initial_energy = energies[0]
    drift = np.abs(np.array(energies) - initial_energy) / initial_energy * 100
    max_drift = np.max(drift)
    mean_drift = np.mean(drift)
    return {'max_drift_%': max_drift, 'mean_drift_%': mean_drift}

energy_metrics = compute_energy_drift(result, dynamics)
print(f"Energy drift: {energy_metrics['max_drift_%']:.3f}% (max), "
      f"{energy_metrics['mean_drift_%']:.3f}% (mean)")