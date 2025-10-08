# Example from: docs\analysis\view_conversion_recommendations.md
# Index: 6
# Runnable: True
# Hash: ead496d0

# CORRECT
def _crossover(self, target: np.ndarray, mutant: np.ndarray) -> np.ndarray:
    trial = target.copy()  # ✅ Required (will mutate)
    j_rand = rng.integers(0, len(target))
    trial[j_rand] = mutant[j_rand]  # In-place mutation
    return trial