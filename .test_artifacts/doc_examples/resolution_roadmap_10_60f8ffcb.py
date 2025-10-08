# Example from: docs\testing\reports\2025-09-30\technical\resolution_roadmap.md
# Index: 10
# Runnable: False
# Hash: 60f8ffcb

# example-metadata:
# runnable: false

# File: src/utils/numerical/robust_matrix_ops.py
class RobustMatrixOperations:
    """Numerically stable matrix operations for control systems."""

    def __init__(self, condition_threshold: float = 1e6, regularization_eps: float = 1e-10):
        self.condition_threshold = condition_threshold
        self.regularization_eps = regularization_eps

    def safe_matrix_inverse(self, matrix: np.ndarray) -> np.ndarray:
        """Numerically stable matrix inversion with fallback methods."""
        try:
            # Check condition number
            condition_number = np.linalg.cond(matrix)

            if condition_number > self.condition_threshold:
                return self._regularized_inverse(matrix)

            # Standard inversion for well-conditioned matrices
            return np.linalg.inv(matrix)

        except np.linalg.LinAlgError:
            # Fallback to pseudoinverse
            return self._robust_pseudoinverse(matrix)

    def _regularized_inverse(self, matrix: np.ndarray) -> np.ndarray:
        """Tikhonov regularization for ill-conditioned matrices."""
        regularization = self.regularization_eps * np.trace(matrix) / matrix.shape[0]
        regularized_matrix = matrix + regularization * np.eye(matrix.shape[0])
        return np.linalg.inv(regularized_matrix)

    def _robust_pseudoinverse(self, matrix: np.ndarray) -> np.ndarray:
        """SVD-based pseudoinverse with numerical thresholding."""
        U, sigma, Vt = np.linalg.svd(matrix, full_matrices=False)

        # Threshold small singular values
        sigma_threshold = self.regularization_eps * np.max(sigma)
        sigma_inv = np.where(sigma > sigma_threshold, 1.0 / sigma, 0.0)

        return Vt.T @ np.diag(sigma_inv) @ U.T

    def safe_division(self, numerator: float, denominator: float) -> float:
        """Division with zero-protection."""
        if abs(denominator) < self.regularization_eps:
            return np.sign(denominator) * numerator / self.regularization_eps
        return numerator / denominator