# Example from: docs\mathematical_foundations\pso_algorithm_theory.md
# Index: 15
# Runnable: True
# Hash: fa9984f1

def compute_diversity(swarm_positions):
    """Measure swarm spread."""
    centroid = np.mean(swarm_positions, axis=0)
    diversity = np.mean([np.linalg.norm(x - centroid)
                        for x in swarm_positions])
    return diversity