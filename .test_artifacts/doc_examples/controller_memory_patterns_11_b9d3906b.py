# Example from: docs\analysis\controller_memory_patterns.md
# Index: 11
# Runnable: True
# Hash: b9d3906b

# ✅ GOOD: Copy only if modifying
state_modified = state.copy()
state_modified[0] = new_value

# ✅ GOOD: In-place operations on views
state[3:] += acceleration * dt  # Safe mutation via view