# Example from: docs\mathematical_foundations\algorithm_fixes_summary.md
# Index: 5
# Runnable: False
# Hash: 6372f53c

# example-metadata:
# runnable: false

   @dataclass(frozen=True)
   class ClassicalSMCConfig:
       """Type-safe configuration with mathematical validation."""

       def __post_init__(self):
           """Validate configuration after creation."""
           self._validate_gains()
           self._validate_parameters()
           self._validate_mathematical_constraints()

       def _validate_gains(self) -> None:
           """Validate gain vector according to SMC theory."""
           if len(self.gains) != 6:
               raise ValueError("Classical SMC requires exactly 6 gains")

           k1, k2, lam1, lam2, K, kd = self.gains

           # Surface gains: positive for Hurwitz stability
           if any(g <= 0 for g in [k1, k2, lam1, lam2]):
               raise ValueError("Surface gains must be positive for stability")

           # Switching gain: positive for reaching condition
           if K <= 0:
               raise ValueError("Switching gain K must be positive")

           # Derivative gain: non-negative for damping
           if kd < 0:
               raise ValueError("Derivative gain kd must be non-negative")

       def _validate_mathematical_constraints(self) -> None:
           """Validate constraints from mathematical theory."""

           # Damping ratio bounds for each subsystem
           zeta1 = self.lam1 / (2 * np.sqrt(self.k1))
           zeta2 = self.lam2 / (2 * np.sqrt(self.k2))

           if zeta1 < 0.1 or zeta2 < 0.1:
               raise ValueError("Damping ratios too low - may cause oscillations")

           if zeta1 > 10.0 or zeta2 > 10.0:
               raise ValueError("Damping ratios too high - may cause sluggish response")