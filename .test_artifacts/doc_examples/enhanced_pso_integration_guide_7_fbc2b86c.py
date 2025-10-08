# Example from: docs\factory\enhanced_pso_integration_guide.md
# Index: 7
# Runnable: False
# Hash: fbc2b86c

# example-metadata:
# runnable: false

class SimulationCache:
    """
    Intelligent caching system for PSO optimization.

    Features:
    - Hash-based lookup for identical gain sets
    - LRU eviction for memory management
    - Cache hit/miss statistics
    - Persistent storage for long-running optimizations
    """

    def __init__(self, max_size: int = 1000, tolerance: float = 1e-6):
        self.cache = {}
        self.max_size = max_size
        self.tolerance = tolerance
        self.hits = 0
        self.misses = 0

    def get_cache_key(self, gains: np.ndarray) -> str:
        """Generate consistent cache key for gain arrays."""
        rounded_gains = np.round(gains / self.tolerance) * self.tolerance
        return hash(tuple(rounded_gains))

    def get(self, gains: np.ndarray) -> Optional[float]:
        """Retrieve cached fitness if available."""
        key = self.get_cache_key(gains)
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None

    def put(self, gains: np.ndarray, fitness: float) -> None:
        """Store fitness result in cache."""
        if len(self.cache) >= self.max_size:
            # Remove oldest entry (simple LRU)
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]

        key = self.get_cache_key(gains)
        self.cache[key] = fitness

    def get_statistics(self) -> Dict[str, Any]:
        """Return cache performance statistics."""
        total_requests = self.hits + self.misses
        hit_rate = self.hits / total_requests if total_requests > 0 else 0

        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'cache_size': len(self.cache)
        }