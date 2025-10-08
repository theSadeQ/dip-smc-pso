# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 20
# Runnable: False
# Hash: 6efff813

# example-metadata:
# runnable: false

# Recommendation: Always use runtime type validation in development
def compute_control(self, ...) -> HybridSTAOutput:
    # ... implementation ...

    result = HybridSTAOutput(...)

    # Development-mode validation
    if __debug__:
        assert isinstance(result, HybridSTAOutput)

    return result