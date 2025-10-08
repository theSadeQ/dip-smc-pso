# Example from: docs\pso_configuration_schema_documentation.md
# Index: 3
# Runnable: False
# Hash: 639f79a1

# example-metadata:
# runnable: false

class ConstraintPropagator:
    """
    Intelligent constraint propagation for interdependent PSO parameters.
    """

    def __init__(self, controller_type: str):
        self.controller_type = controller_type
        self.constraint_graph = self._build_constraint_graph()

    def propagate_constraints(self, initial_bounds: dict) -> dict:
        """
        Propagate constraints through parameter dependency graph.

        Example: If λ₁ is constrained to [0.1, 5.0] for Issue #2,
        then c₁ bounds must ensure ζ₁ = λ₁/(2√c₁) ∈ [0.69, 0.8]
        """
        propagated_bounds = initial_bounds.copy()

        # Iterative constraint propagation
        converged = False
        max_iterations = 10
        iteration = 0

        while not converged and iteration < max_iterations:
            old_bounds = propagated_bounds.copy()

            # Apply constraint rules
            for constraint in self.constraint_graph:
                propagated_bounds = self._apply_constraint_rule(
                    constraint, propagated_bounds
                )

            # Check convergence
            converged = self._bounds_converged(old_bounds, propagated_bounds)
            iteration += 1

        return propagated_bounds

    def _apply_constraint_rule(self, constraint: dict, bounds: dict) -> dict:
        """
        Apply individual constraint rule with mathematical validation.
        """
        if constraint['type'] == 'damping_ratio':
            # ζ = λ/(2√c) constraint propagation
            lambda_idx = constraint['lambda_idx']
            c_idx = constraint['c_idx']
            target_zeta_range = constraint['zeta_range']

            lambda_min, lambda_max = bounds['min'][lambda_idx], bounds['max'][lambda_idx]

            # Derive c bounds from lambda bounds and zeta constraints
            # For ζ_min ≤ λ/(2√c) ≤ ζ_max:
            # c_min = (λ/(2ζ_max))², c_max = (λ/(2ζ_min))²

            c_min_from_lambda = (lambda_min / (2 * target_zeta_range[1]))**2
            c_max_from_lambda = (lambda_max / (2 * target_zeta_range[0]))**2

            # Update c bounds with constraint propagation
            bounds['min'][c_idx] = max(bounds['min'][c_idx], c_min_from_lambda)
            bounds['max'][c_idx] = min(bounds['max'][c_idx], c_max_from_lambda)

        elif constraint['type'] == 'sta_stability':
            # K₁ > K₂ constraint with margin
            k1_idx, k2_idx = constraint['k1_idx'], constraint['k2_idx']
            margin = constraint.get('margin', 0.1)

            # Ensure K₁_min > K₂_max + margin
            bounds['min'][k1_idx] = max(
                bounds['min'][k1_idx],
                bounds['max'][k2_idx] + margin
            )

        return bounds

    def _build_constraint_graph(self) -> list:
        """
        Build constraint dependency graph for controller type.
        """
        if self.controller_type == 'classical_smc':
            return [
                {
                    'type': 'damping_ratio',
                    'lambda_idx': 1, 'c_idx': 0,
                    'zeta_range': [0.6, 0.8]
                },
                {
                    'type': 'damping_ratio',
                    'lambda_idx': 3, 'c_idx': 2,
                    'zeta_range': [0.6, 0.8]
                },
                {
                    'type': 'actuator_saturation',
                    'gain_indices': [4, 5],  # K, kd
                    'max_total': 150.0
                }
            ]

        elif self.controller_type == 'sta_smc':
            return [
                {
                    'type': 'sta_stability',
                    'k1_idx': 0, 'k2_idx': 1,
                    'margin': 0.1
                },
                {
                    'type': 'damping_ratio',
                    'lambda_idx': 4, 'c_idx': 2,  # lambda1, k1
                    'zeta_range': [0.69, 0.8]  # Issue #2 requirement
                },
                {
                    'type': 'damping_ratio',
                    'lambda_idx': 5, 'c_idx': 3,  # lambda2, k2
                    'zeta_range': [0.69, 0.8]  # Issue #2 requirement
                }
            ]

        return []