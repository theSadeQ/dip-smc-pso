# Example from: docs\mathematical_algorithm_validation.md
# Index: 7
# Runnable: True
# Hash: 1849dfe5

# Mathematical definition: s = λ₁e₁ + λ₂e₂ + ė₁ + ė₂
def compute_sliding_surface(self, state, target):
    e1 = state[0] - target[0]  # θ₁ error
    e2 = state[1] - target[1]  # θ₂ error
    e1_dot = state[3] - target[3]  # θ̇₁ error
    e2_dot = state[4] - target[4]  # θ̇₂ error

    return self.lambda1 * e1 + self.lambda2 * e2 + e1_dot + e2_dot