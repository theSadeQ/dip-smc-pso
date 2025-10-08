# Example from: docs\quality_gate_independence_framework.md
# Index: 8
# Runnable: False
# Hash: 55682725

class DeploymentDecisionEngine:
    """Makes deployment decisions based on independent validation results."""

    def __init__(self):
        self.decision_criteria = {
            'safety_critical_coverage': {
                'weight': 0.25,
                'threshold': 100.0,  # Must be 100%
                'tolerance': 0.0     # No tolerance for safety-critical
            },
            'mathematical_validation': {
                'weight': 0.25,
                'threshold': 0.9,    # 90% mathematical validation
                'tolerance': 0.1     # Small tolerance allowed
            },
            'critical_coverage': {
                'weight': 0.20,
                'threshold': 95.0,   # 95% coverage
                'tolerance': 0.05    # 5% tolerance
            },
            'performance_validation': {
                'weight': 0.15,
                'threshold': 0.8,    # 80% performance validation
                'tolerance': 0.2     # 20% tolerance
            },
            'compliance_validation': {
                'weight': 0.10,
                'threshold': 0.85,   # 85% compliance
                'tolerance': 0.15    # 15% tolerance
            },
            'general_coverage': {
                'weight': 0.05,
                'threshold': 85.0,   # 85% coverage
                'tolerance': 0.15    # 15% tolerance
            }
        }

    def make_deployment_decision(self,
                               validation_results: IndependentValidationResults) -> DeploymentDecision:
        """Make deployment decision based on independent validation results."""

        # Extract criteria values from validation results
        criteria_values = self._extract_criteria_values(validation_results)

        # Evaluate each criterion
        criterion_evaluations = {}
        for criterion, config in self.decision_criteria.items():
            evaluation = self._evaluate_criterion(
                criterion,
                criteria_values.get(criterion, 0.0),
                config
            )
            criterion_evaluations[criterion] = evaluation

        # Calculate weighted deployment score
        deployment_score = self._calculate_deployment_score(criterion_evaluations)

        # Make deployment decision
        deployment_decision = self._determine_deployment_status(
            deployment_score, criterion_evaluations
        )

        # Generate deployment conditions and recommendations
        deployment_conditions = self._generate_deployment_conditions(criterion_evaluations)

        return DeploymentDecision(
            decision=deployment_decision,
            score=deployment_score,
            criterion_evaluations=criterion_evaluations,
            deployment_conditions=deployment_conditions,
            risk_assessment=self._assess_deployment_risk(
                deployment_score, criterion_evaluations
            ),
            rollback_plan=self._generate_rollback_plan(criterion_evaluations),
            monitoring_requirements=self._define_monitoring_requirements(
                deployment_decision, criterion_evaluations
            )
        )

    def _determine_deployment_status(self,
                                   deployment_score: float,
                                   criterion_evaluations: Dict[str, CriterionEvaluation]) -> str:
        """Determine deployment status based on score and critical failures."""

        # Check for critical failures that block deployment
        critical_failures = []

        # Safety-critical coverage must be 100%
        safety_critical_eval = criterion_evaluations.get('safety_critical_coverage')
        if safety_critical_eval and not safety_critical_eval.passed:
            critical_failures.append('safety_critical_coverage_failed')

        # Mathematical validation is critical for correctness
        mathematical_eval = criterion_evaluations.get('mathematical_validation')
        if mathematical_eval and mathematical_eval.score < 0.7:  # Minimum mathematical validation
            critical_failures.append('mathematical_validation_insufficient')

        # If any critical failures, deployment is blocked
        if critical_failures:
            return 'blocked'

        # Deployment decision based on overall score
        if deployment_score >= 0.9:
            return 'approved'
        elif deployment_score >= 0.8:
            return 'conditional_approval'
        elif deployment_score >= 0.7:
            return 'conditional_approval_with_monitoring'
        else:
            return 'rejected'

    def _generate_deployment_conditions(self,
                                      criterion_evaluations: Dict[str, CriterionEvaluation]) -> List[DeploymentCondition]:
        """Generate specific deployment conditions based on evaluation results."""

        conditions = []

        # Check for conditions based on specific criterion failures
        for criterion, evaluation in criterion_evaluations.items():
            if not evaluation.passed:
                if criterion == 'safety_critical_coverage':
                    conditions.append(DeploymentCondition(
                        type='blocking',
                        description='Safety-critical coverage must reach 100% before deployment',
                        required_action='Complete safety-critical test coverage',
                        estimated_effort='high',
                        priority='critical'
                    ))

                elif criterion == 'mathematical_validation':
                    conditions.append(DeploymentCondition(
                        type='conditional',
                        description='Mathematical validation below threshold',
                        required_action='Complete mathematical property verification',
                        estimated_effort='medium',
                        priority='high'
                    ))

                elif criterion == 'performance_validation':
                    conditions.append(DeploymentCondition(
                        type='monitoring',
                        description='Performance validation partial - requires monitoring',
                        required_action='Implement performance monitoring in production',
                        estimated_effort='low',
                        priority='medium'
                    ))

        return conditions