# Example from: docs\fault_detection_system_documentation.md
# Index: 14
# Runnable: True
# Hash: 52bb675b

# CORRECT: Element-wise weight multiplication before norm
sub = residual[self.residual_states]
if weights is not None:
    sub = sub * np.asarray(weights, dtype=float)  # Element-wise multiplication
residual_norm = float(np.linalg.norm(sub))        # Then compute norm