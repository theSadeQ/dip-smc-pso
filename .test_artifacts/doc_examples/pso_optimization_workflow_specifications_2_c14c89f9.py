# Example from: docs\pso_optimization_workflow_specifications.md
# Index: 2
# Runnable: False
# Hash: c14c89f9

class BoundsValidator:
    """
    Advanced bounds validation with constraint propagation.
    """

    def validate_and_propagate_bounds(self, config: dict,
                                    controller_type: str) -> BoundsValidationResult:
        """
        Validate bounds and propagate mathematical constraints.

        Constraint Propagation Rules:
        1. Damping ratio constraints: ζ = λ/(2√c) ∈ [0.6, 0.8]
        2. STA stability: K₁ > K₂ for finite-time convergence
        3. Actuator saturation: ∑gains ≤ 150 N
        4. Issue #2 compliance: ζ ≥ 0.69 for STA-SMC
        """
        result = BoundsValidationResult()

        bounds_config = config.get('pso', {}).get('bounds', {})
        controller_bounds = bounds_config.get(controller_type, bounds_config)

        if 'min' not in controller_bounds or 'max' not in controller_bounds:
            result.errors.append('Missing min/max bounds for controller')
            result.is_valid = False
            return result

        min_bounds = np.array(controller_bounds['min'])
        max_bounds = np.array(controller_bounds['max'])

        # Basic bounds validation
        if len(min_bounds) != len(max_bounds):
            result.errors.append('Min/max bounds length mismatch')
            result.is_valid = False
            return result

        invalid_bounds = min_bounds >= max_bounds
        if np.any(invalid_bounds):
            invalid_indices = np.where(invalid_bounds)[0]
            result.errors.append(f'Invalid bounds at indices: {invalid_indices.tolist()}')
            result.is_valid = False

        # Controller-specific constraint propagation
        if controller_type == 'classical_smc' and len(min_bounds) >= 6:
            propagated_bounds = self._propagate_classical_smc_constraints(min_bounds, max_bounds)
            result.propagated_bounds = propagated_bounds
            result.constraint_violations = self._check_classical_smc_constraints(propagated_bounds)

        elif controller_type == 'sta_smc' and len(min_bounds) >= 6:
            propagated_bounds = self._propagate_sta_smc_constraints(min_bounds, max_bounds)
            result.propagated_bounds = propagated_bounds
            result.constraint_violations = self._check_sta_smc_constraints(propagated_bounds)

            # Issue #2 specific validation
            lambda1_max, lambda2_max = propagated_bounds[1][4], propagated_bounds[1][5]
            if lambda1_max > 10.0 or lambda2_max > 10.0:
                result.warnings.append(f'Issue #2 risk: lambda bounds [{lambda1_max}, {lambda2_max}] > 10.0')

        result.is_valid = len(result.errors) == 0 and len(result.constraint_violations) == 0
        return result

    def _propagate_sta_smc_constraints(self, min_bounds: np.ndarray,
                                     max_bounds: np.ndarray) -> tuple:
        """
        Propagate STA-SMC mathematical constraints through bounds.

        Constraints:
        1. K₁ > K₂ (stability condition)
        2. ζ = λ/(2√k) ∈ [0.69, 0.8] (Issue #2 damping requirement)
        3. K₁² > 4K₂L (finite-time convergence)
        """
        prop_min = min_bounds.copy()
        prop_max = max_bounds.copy()

        # K₁ > K₂ constraint propagation
        # Ensure K₁_min > K₂_max + margin
        margin = 0.1
        if prop_max[1] + margin > prop_min[0]:
            prop_min[0] = prop_max[1] + margin

        # Damping ratio constraint propagation (Issue #2)
        # For ζ = λ/(2√k) ∈ [0.69, 0.8]:
        target_zeta_min, target_zeta_max = 0.69, 0.8

        # k₁, λ₁ relationship
        k1_min, k1_max = prop_min[2], prop_max[2]
        lambda1_min, lambda1_max = prop_min[4], prop_max[4]

        # Propagate k₁ bounds from λ₁ bounds and ζ constraints
        k1_min_from_lambda = (lambda1_min / (2 * target_zeta_max))**2
        k1_max_from_lambda = (lambda1_max / (2 * target_zeta_min))**2

        prop_min[2] = max(prop_min[2], k1_min_from_lambda)
        prop_max[2] = min(prop_max[2], k1_max_from_lambda)

        # Similarly for k₂, λ₂
        k2_min_from_lambda = (prop_min[5] / (2 * target_zeta_max))**2
        k2_max_from_lambda = (prop_max[5] / (2 * target_zeta_min))**2

        prop_min[3] = max(prop_min[3], k2_min_from_lambda)
        prop_max[3] = min(prop_max[3], k2_max_from_lambda)

        return prop_min, prop_max

    def _check_sta_smc_constraints(self, bounds: tuple) -> list:
        """
        Check STA-SMC constraint violations after propagation.
        """
        min_bounds, max_bounds = bounds
        violations = []

        # Check if K₁ > K₂ is feasible
        if min_bounds[0] <= max_bounds[1]:
            violations.append('STA stability constraint K₁ > K₂ not satisfiable with given bounds')

        # Check damping ratio feasibility
        for i, (k_idx, lambda_idx) in enumerate([(2, 4), (3, 5)]):  # (k₁,λ₁), (k₂,λ₂)
            k_min, k_max = min_bounds[k_idx], max_bounds[k_idx]
            lambda_min, lambda_max = min_bounds[lambda_idx], max_bounds[lambda_idx]

            # Check if target damping range [0.69, 0.8] is achievable
            zeta_min_possible = lambda_min / (2 * np.sqrt(k_max))
            zeta_max_possible = lambda_max / (2 * np.sqrt(k_min))

            if zeta_max_possible < 0.69:
                violations.append(f'Damping ratio {i+1} cannot achieve ζ ≥ 0.69 (Issue #2 requirement)')
            if zeta_min_possible > 0.8:
                violations.append(f'Damping ratio {i+1} cannot achieve ζ ≤ 0.8')

        return violations