# Example from: docs\troubleshooting\hybrid_smc_runtime_fix_final.md
# Index: 2
# Runnable: False
# Hash: 4ab70ff5

# Added comprehensive result normalization with array detection
def _normalize_result(self, result):
    """Ensure result is properly formatted as HybridSTAOutput."""
    if result is None:
        # Emergency fallback for None returns
        return HybridSTAOutput(
            control=0.0,
            state_vars=(self.k1_init, self.k2_init, 0.0),
            history=self.initialize_history(),
            sliding_surface=0.0
        )

    if isinstance(result, np.ndarray):
        # Convert numpy array to dictionary structure
        return self._array_to_output(result)

    return result