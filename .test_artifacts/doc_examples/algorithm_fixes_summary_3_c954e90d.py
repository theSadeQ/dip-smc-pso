# Example from: docs\mathematical_foundations\algorithm_fixes_summary.md
# Index: 3
# Runnable: False
# Hash: c954e90d

def compute(self, state: np.ndarray) -> float:
       """Compute linear sliding surface with numerical safeguards."""

       # Input validation
       if len(state) < 6:
           raise ValueError("State must have at least 6 elements")

       # Handle non-finite values
       if not np.all(np.isfinite(state)):
           state = np.where(np.isfinite(state), state, 0.0)

       # Extract components
       theta1, theta1_dot = state[2], state[3]
       theta2, theta2_dot = state[4], state[5]

       # Linear sliding surface: s = λ₁θ̇₁ + k₁θ₁ + λ₂θ̇₂ + k₂θ₂
       s = (self.lam1 * theta1_dot + self.k1 * theta1 +
            self.lam2 * theta2_dot + self.k2 * theta2)

       # Numerical safety
       return 0.0 if not np.isfinite(s) else float(s)