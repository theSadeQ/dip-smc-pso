# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 12
# Runnable: False
# Hash: 0d81dd43

def compute_diversity(self) -> float:
    """Compute swarm diversity metric.

    Returns:
        Diversity value (normalized)
    """
    # Swarm centroid
    centroid = np.mean(self.positions, axis=0)

    # Average distance from centroid
    distances = [
        np.linalg.norm(pos - centroid)
        for pos in self.positions
    ]
    diversity = np.mean(distances)

    # Normalize by search space diagonal
    diagonal = np.linalg.norm(self.bounds_upper - self.bounds_lower)
    diversity_normalized = diversity / diagonal

    return diversity_normalized