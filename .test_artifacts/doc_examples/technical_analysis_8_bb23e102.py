# Example from: docs\testing\reports\2025-09-30\technical_analysis.md
# Index: 8
# Runnable: False
# Hash: bb23e102

def analyze_matrix_conditioning():
    """Analysis of matrix conditioning problems."""

    # Problem matrices encountered in testing
    problematic_matrices = [
        np.array([[1.0, 1.0], [1.0, 1.0000001]]),  # Nearly singular
        np.array([[1e-8, 0], [0, 1.0]]),           # Poorly scaled
        np.array([[1.0, 1e8], [1e-8, 1.0]])       # Wide dynamic range
    ]

    for i, matrix in enumerate(problematic_matrices):
        cond_num = np.linalg.cond(matrix)
        if cond_num > 1e12:
            print(f"Matrix {i}: Condition number {cond_num:.2e} (CRITICAL)")

            # Propose regularization
            regularized = matrix + np.eye(matrix.shape[0]) * 1e-6
            new_cond = np.linalg.cond(regularized)
            print(f"  Regularized: {new_cond:.2e}")