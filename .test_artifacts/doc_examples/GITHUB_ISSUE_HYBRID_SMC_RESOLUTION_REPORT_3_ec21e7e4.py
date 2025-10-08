# Example from: docs\reports\GITHUB_ISSUE_HYBRID_SMC_RESOLUTION_REPORT.md
# Index: 3
# Runnable: False
# Hash: ec21e7e4

# example-metadata:
# runnable: false

def _normalize_result(self, result):
    """Ensure result is properly formatted as HybridSTAOutput."""
    if result is None:
        # Emergency fallback for None returns
        logger.warning("Controller returned None - using emergency fallback")
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