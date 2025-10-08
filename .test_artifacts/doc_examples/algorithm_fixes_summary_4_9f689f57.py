# Example from: docs\mathematical_foundations\algorithm_fixes_summary.md
# Index: 4
# Runnable: False
# Hash: 9f689f57

def _validate_gains(self) -> None:
       """Validate gains according to Hurwitz stability requirements."""

       # Check finite values
       if not np.all(np.isfinite(self.gains)):
           invalid_indices = np.where(~np.isfinite(self.gains))[0]
           raise ValueError(f"Gains contain NaN/infinite values at indices: {invalid_indices}")

       # Positivity requirement for stability
       if len(self.gains) >= 4:
           if any(g <= 0 for g in self.gains[:4]):
               raise ValueError("Surface gains [k1, k2, λ1, λ2] must be positive for stability")

       # Minimum threshold for numerical stability
       if any(g < 1e-12 for g in self.gains[:4]):
           raise ValueError("Gains too small (min: 1e-12) - numerical instability risk")