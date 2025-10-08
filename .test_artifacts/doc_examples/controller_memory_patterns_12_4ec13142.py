# Example from: docs\analysis\controller_memory_patterns.md
# Index: 12
# Runnable: True
# Hash: 4ec13142

# ✅ GOOD: Scalar extraction
x = state[0]
theta1 = state[1]

# ⚠️ AVOID: Array slicing for single elements
x = state[0:1]  # Returns array, not scalar