# Example from: docs\analysis\controller_memory_patterns.md
# Index: 10
# Runnable: True
# Hash: d4a1c612

# ✅ GOOD: Direct unpacking
x, theta1, theta2, xdot, theta1dot, theta2dot = state

# ✅ GOOD: Slicing for vectors
velocities = state[3:]  # View
positions = state[:3]   # View

# ❌ BAD: Unnecessary copying
velocities = state[3:].copy()  # Only if mutating!