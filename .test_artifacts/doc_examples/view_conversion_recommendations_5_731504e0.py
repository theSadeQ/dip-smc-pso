# Example from: docs\analysis\view_conversion_recommendations.md
# Index: 5
# Runnable: True
# Hash: 731504e0

# CORRECT
for i in range(n):
    state_plus = eq_state.copy()  # ✅ Required (will mutate)
    state_plus[i] += eps
    dynamics_plus = self.compute_dynamics(state_plus, eq_input)