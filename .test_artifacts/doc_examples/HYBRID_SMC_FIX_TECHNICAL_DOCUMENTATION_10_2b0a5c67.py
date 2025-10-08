# Example from: docs\analysis\HYBRID_SMC_FIX_TECHNICAL_DOCUMENTATION.md
# Index: 10
# Runnable: False
# Hash: 2b0a5c67

# Add runtime type validation
def compute_control(self, ...) -> HybridSTAOutput:
    # ... implementation ...
    result = HybridSTAOutput(...)

    # Development mode validation
    if __debug__:
        assert isinstance(result, HybridSTAOutput)
        assert hasattr(result, 'control')
        assert isinstance(result.control, (int, float))

    return result