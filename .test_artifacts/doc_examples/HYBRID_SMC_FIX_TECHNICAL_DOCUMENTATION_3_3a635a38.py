# Example from: docs\analysis\HYBRID_SMC_FIX_TECHNICAL_DOCUMENTATION.md
# Index: 3
# Runnable: False
# Hash: 3a635a38

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