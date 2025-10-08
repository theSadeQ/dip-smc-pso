# Example from: docs\testing\reports\2025-09-30\technical_analysis.md
# Index: 10
# Runnable: False
# Hash: 542c164e

# example-metadata:
# runnable: false

# 1. Enhanced Matrix Operations
class RobustMatrixOps:
    """Numerically stable matrix operations."""

    @staticmethod
    def safe_inverse(matrix, regularization=1e-12):
        """Compute matrix inverse with automatic regularization."""
        cond_num = np.linalg.cond(matrix)

        if cond_num > 1e12:
            # Apply Tikhonov regularization
            regularized = matrix + np.eye(matrix.shape[0]) * regularization
            return np.linalg.inv(regularized)
        else:
            return np.linalg.inv(matrix)

    @staticmethod
    def robust_solve(A, b, regularization=1e-12):
        """Solve linear system with enhanced stability."""
        try:
            # Try standard solution first
            return np.linalg.solve(A, b)
        except LinAlgError:
            # Fallback to regularized solution
            A_reg = A + np.eye(A.shape[0]) * regularization
            return np.linalg.solve(A_reg, b)

    @staticmethod
    def safe_division(numerator, denominator, epsilon=1e-12):
        """Division with zero-protection."""
        safe_denom = np.where(np.abs(denominator) < epsilon,
                             np.sign(denominator) * epsilon,
                             denominator)
        return numerator / safe_denom

# 2. Numerically Stable SMC Implementation
class NumericallyStableSMC:
    """SMC controller with enhanced numerical stability."""

    def __init__(self, gains, max_force, boundary_layer=0.01):
        self.gains = np.asarray(gains)
        self.max_force = max_force
        self.boundary_layer = max(boundary_layer, 1e-6)  # Prevent zero boundary
        self.matrix_ops = RobustMatrixOps()

    def compute_sliding_surface(self, state):
        """Numerically stable sliding surface computation."""
        # Enhanced precision for critical calculations
        state_hp = np.array(state, dtype=np.float64)  # High precision

        # Compute sliding surface with overflow protection
        surface_terms = []
        for i, gain in enumerate(self.gains):
            if i < len(state_hp):
                term = gain * state_hp[i]
                # Prevent overflow
                if np.abs(term) > 1e6:
                    term = np.sign(term) * 1e6
                surface_terms.append(term)

        surface = np.sum(surface_terms)

        # Prevent numerical underflow
        if np.abs(surface) < 1e-15:
            surface = 0.0

        return surface

    def robust_switching_function(self, surface):
        """Switching function with enhanced stability."""
        # Use tanh for smooth switching with numerical stability
        normalized_surface = surface / self.boundary_layer

        # Prevent overflow in exponential
        if np.abs(normalized_surface) > 50:
            return np.sign(normalized_surface)

        return np.tanh(normalized_surface)

# 3. Adaptive Numerical Precision
class AdaptivePrecisionController:
    """Controller that adjusts numerical precision based on conditioning."""

    def __init__(self, base_precision=np.float64):
        self.base_precision = base_precision
        self.high_precision = np.longdouble  # Higher precision for critical ops
        self.precision_threshold = 1e10  # Condition number threshold

    def compute_control_adaptive_precision(self, state, gains):
        """Adaptively adjust precision based on numerical conditioning."""

        # Compute condition number estimate
        state_matrix = np.outer(state, gains)
        cond_estimate = np.linalg.cond(state_matrix)

        if cond_estimate > self.precision_threshold:
            # Use high precision for ill-conditioned problems
            state_hp = np.array(state, dtype=self.high_precision)
            gains_hp = np.array(gains, dtype=self.high_precision)
            control_hp = self._compute_control(state_hp, gains_hp)
            return np.array(control_hp, dtype=self.base_precision)
        else:
            # Standard precision sufficient
            return self._compute_control(state, gains)