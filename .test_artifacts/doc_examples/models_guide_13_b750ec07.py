# Example from: docs\plant\models_guide.md
# Index: 13
# Runnable: False
# Hash: b750ec07

class MatrixInverter:
    """Robust matrix inversion with regularization."""

    def solve_linear_system(
        self,
        A: np.ndarray,
        b: np.ndarray
    ) -> np.ndarray:
        """Solve Ax = b with adaptive regularization."""

        try:
            # Attempt direct solution
            return np.linalg.solve(A, b)

        except np.linalg.LinAlgError:
            # Apply adaptive regularization
            alpha = self.regularizer.compute_regularization(A)
            A_reg = A + alpha * np.eye(A.shape[0])

            try:
                return np.linalg.solve(A_reg, b)
            except np.linalg.LinAlgError:
                # Use pseudo-inverse as last resort
                return np.linalg.lstsq(A_reg, b, rcond=None)[0]