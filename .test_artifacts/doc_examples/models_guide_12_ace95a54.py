# Example from: docs\plant\models_guide.md
# Index: 12
# Runnable: False
# Hash: ace95a54

# example-metadata:
# runnable: false

class AdaptiveRegularizer:
    """Adaptive regularization for matrix conditioning."""

    def compute_regularization(self, matrix: np.ndarray) -> float:
        """Compute adaptive regularization parameter."""

        # Compute condition number
        cond_num = np.linalg.cond(matrix)

        if cond_num > self.max_condition_number:
            # Adaptive regularization scaled by condition number
            alpha = self.regularization_alpha * (cond_num / self.max_condition_number)
            return max(alpha, self.min_regularization)
        else:
            # Use fixed minimal regularization
            return self.min_regularization