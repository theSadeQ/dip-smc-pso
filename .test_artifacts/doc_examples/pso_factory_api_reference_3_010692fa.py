# Example from: docs\factory\pso_factory_api_reference.md
# Index: 3
# Runnable: False
# Hash: 010692fa

@dataclass(frozen=True)
class SMCGainSpec:
    """
    Complete specification for SMC controller gains.

    Provides comprehensive information about gain parameters including
    mathematical meaning, constraints, and PSO optimization bounds.
    """

    controller_type: SMCType
    n_gains: int
    gain_names: List[str]
    gain_descriptions: List[str]
    mathematical_constraints: List[str]
    pso_bounds: List[Tuple[float, float]]
    default_gains: List[float]

    @property
    def gain_info(self) -> List[Dict[str, Any]]:
        """
        Return comprehensive gain information.

        Returns:
            List of dictionaries containing:
                - name: Parameter name
                - description: Mathematical meaning
                - constraint: Mathematical constraint
                - bounds: PSO optimization bounds
                - default: Default value
        """
        return [
            {
                'name': name,
                'description': desc,
                'constraint': constraint,
                'bounds': bounds,
                'default': default
            }
            for name, desc, constraint, bounds, default in zip(
                self.gain_names,
                self.gain_descriptions,
                self.mathematical_constraints,
                self.pso_bounds,
                self.default_gains
            )
        ]

    def validate_gains(self, gains: List[float]) -> Tuple[bool, List[str]]:
        """
        Validate gains against mathematical constraints.

        Args:
            gains: Gain values to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        if len(gains) != self.n_gains:
            errors.append(f"Expected {self.n_gains} gains, got {len(gains)}")
            return False, errors

        # Controller-specific validation
        if self.controller_type == SMCType.CLASSICAL:
            if any(g <= 0 for g in gains[:5]):  # k1,k2,λ1,λ2,K > 0
                errors.append("Surface and switching gains must be positive")
            if gains[5] < 0:  # kd ≥ 0
                errors.append("Damping gain must be non-negative")

        elif self.controller_type == SMCType.SUPER_TWISTING:
            if gains[0] <= gains[1]:  # K1 > K2
                errors.append("K1 must be greater than K2 for convergence")
            if any(g <= 0 for g in gains):  # All gains > 0
                errors.append("All STA gains must be positive")

        elif self.controller_type == SMCType.ADAPTIVE:
            if any(g <= 0 for g in gains[:4]):  # k1,k2,λ1,λ2 > 0
                errors.append("Surface gains must be positive")
            if not (0.1 <= gains[4] <= 20.0):  # γ bounds
                errors.append("Adaptation rate must be in [0.1, 20.0]")

        elif self.controller_type == SMCType.HYBRID:
            if any(g <= 0 for g in gains):  # All gains > 0
                errors.append("All hybrid gains must be positive")

        return len(errors) == 0, errors

    def get_pso_bounds_array(self) -> np.ndarray:
        """Return PSO bounds as numpy array for optimization algorithms."""
        return np.array(self.pso_bounds)

    def get_random_valid_gains(self, n_samples: int = 1) -> np.ndarray:
        """
        Generate random valid gain sets within PSO bounds.

        Useful for PSO initialization and testing.

        Args:
            n_samples: Number of random gain sets to generate

        Returns:
            Array of shape (n_samples, n_gains) with valid gain sets
        """
        bounds_array = self.get_pso_bounds_array()
        lower_bounds = bounds_array[:, 0]
        upper_bounds = bounds_array[:, 1]

        samples = []
        for _ in range(n_samples):
            while True:
                # Generate random sample in bounds
                sample = np.random.uniform(lower_bounds, upper_bounds)

                # Validate constraints
                is_valid, _ = self.validate_gains(sample.tolist())
                if is_valid:
                    samples.append(sample)
                    break

        return np.array(samples)